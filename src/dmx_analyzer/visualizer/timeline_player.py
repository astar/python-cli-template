"""Real-time timeline player with audio synchronization."""

from __future__ import annotations

import time
from pathlib import Path
from typing import Dict, List, Optional

import pygame
from threading import Thread, Event
import numpy as np

from ..models import DMXTimeline, DMXEvent
from ..logging import get_logger

logger = get_logger(__name__)


class TimelinePlayer:
    """Real-time přehrávač timeline s audio synchronizací."""
    
    def __init__(self, timeline_path: Path, audio_path: Path):
        """Initialize timeline player.
        
        Args:
            timeline_path: Cesta k .tml souboru
            audio_path: Cesta k audio souboru
        """
        self.timeline_path = timeline_path
        self.audio_path = audio_path
        
        # Pygame mixer pro audio
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        
        # Timeline data
        self.timeline: Optional[DMXTimeline] = None
        self.events: List[DMXEvent] = []
        self.active_events: Dict[int, DMXEvent] = {}  # timeline_index -> event
        
        # Playback state
        self.is_playing = False
        self.start_time = 0.0
        self.current_time = 0.0
        self.duration = 0.0
        
        # Threading
        self.update_thread: Optional[Thread] = None
        self.stop_event = Event()
        
        # Callbacks
        self.on_light_change = None  # Callback pro změny světel
        self.on_time_update = None   # Callback pro čas
        
        self._load_timeline()
        self._load_audio()
    
    def _load_timeline(self) -> None:
        """Načte timeline ze souboru."""
        try:
            # Parse .tml file
            self.timeline = self._parse_tml_file(self.timeline_path)
            self.events = self.timeline.events
            
            # Seřaď události podle času
            self.events.sort(key=lambda e: self._time_to_seconds(e.start_time))
            
            logger.info(f"Loaded timeline with {len(self.events)} events")
            
        except Exception as e:
            logger.error(f"Failed to load timeline: {e}")
            raise
    
    def _load_audio(self) -> None:
        """Načte audio soubor."""
        try:
            # Load audio file with pygame
            pygame.mixer.music.load(str(self.audio_path))
            
            # Get duration (approximation)
            import librosa
            y, sr = librosa.load(str(self.audio_path), sr=None)
            self.duration = len(y) / sr
            
            logger.info(f"Loaded audio: {self.duration:.1f}s")
            
        except Exception as e:
            logger.error(f"Failed to load audio: {e}")
            raise
    
    def _parse_tml_file(self, tml_path: Path) -> DMXTimeline:
        """Parse .tml soubor."""
        import configparser
        
        config = configparser.ConfigParser()
        config.read(tml_path, encoding='utf-8')
        
        # Create timeline
        timeline = DMXTimeline()
        
        # Parse events
        events = []
        for section_name in config.sections():
            if section_name.startswith('Event_') and section_name != 'Event_0':
                section = config[section_name]
                
                event = DMXEvent(
                    timeline_index=int(section.get('TimeLineIndex', 3)),
                    start_time=section.get('StartTime', '0:00:00.0'),
                    path=section.get('Path', ''),
                    length=section.get('Length', None),
                    speed=int(section.get('Speed', 100)),
                    fade_in=int(section.get('FadeIn', 0)) if section.get('FadeIn') else None,
                    fade_out=int(section.get('FadeOut', 0)) if section.get('FadeOut') else None,
                    bpm=int(section.get('BPM', 0)) if section.get('BPM') else None
                )
                events.append(event)
        
        timeline.events = events
        return timeline
    
    def play(self) -> None:
        """Spustí přehrávání."""
        if self.is_playing:
            return
        
        self.is_playing = True
        self.start_time = time.time()
        self.stop_event.clear()
        
        # Start audio
        pygame.mixer.music.play()
        
        # Start update thread
        self.update_thread = Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
        
        logger.info("Playback started")
    
    def pause(self) -> None:
        """Pozastaví přehrávání."""
        if not self.is_playing:
            return
        
        self.is_playing = False
        pygame.mixer.music.pause()
        
        logger.info("Playback paused")
    
    def resume(self) -> None:
        """Obnoví přehrávání."""
        if self.is_playing:
            return
        
        self.is_playing = True
        self.start_time = time.time() - self.current_time
        pygame.mixer.music.unpause()
        
        logger.info("Playback resumed")
    
    def stop(self) -> None:
        """Zastaví přehrávání."""
        self.is_playing = False
        self.stop_event.set()
        
        pygame.mixer.music.stop()
        
        if self.update_thread:
            self.update_thread.join(timeout=1.0)
        
        self.current_time = 0.0
        self.active_events.clear()
        
        logger.info("Playback stopped")
    
    def seek(self, time_seconds: float) -> None:
        """Přejde na specifický čas."""
        was_playing = self.is_playing
        
        if self.is_playing:
            self.pause()
        
        self.current_time = max(0, min(time_seconds, self.duration))
        
        # Update active events for new time
        self._update_active_events()
        
        # Seek audio (pygame doesn't support seeking, would need different library)
        # For now, restart from beginning
        if was_playing:
            pygame.mixer.music.play(start=self.current_time)
            self.start_time = time.time() - self.current_time
            self.is_playing = True
    
    def _update_loop(self) -> None:
        """Hlavní update smyčka."""
        while not self.stop_event.is_set() and self.is_playing:
            # Update current time
            self.current_time = time.time() - self.start_time
            
            # Check if we've reached the end
            if self.current_time >= self.duration:
                self.stop()
                break
            
            # Update active events
            self._update_active_events()
            
            # Call time update callback
            if self.on_time_update:
                self.on_time_update(self.current_time, self.duration)
            
            # Sleep for smooth update rate (60 FPS)
            time.sleep(1.0 / 60.0)
    
    def _update_active_events(self) -> None:
        """Aktualizuje aktivní události pro aktuální čas."""
        new_active_events = {}
        light_changes = {}
        
        for event in self.events:
            event_start = self._time_to_seconds(event.start_time)
            
            # Calculate event end time
            if event.length:
                event_duration = self._time_to_seconds(event.length)
                event_end = event_start + event_duration
            else:
                event_end = event_start + 5.0  # Default duration
            
            # Check if event is active at current time
            if event_start <= self.current_time <= event_end:
                new_active_events[event.timeline_index] = event
                
                # Check if this is a new event
                if event.timeline_index not in self.active_events:
                    light_changes[event.timeline_index] = {
                        'event': event,
                        'action': 'start',
                        'progress': (self.current_time - event_start) / (event_end - event_start)
                    }
                else:
                    # Update progress for existing event
                    light_changes[event.timeline_index] = {
                        'event': event,
                        'action': 'update',
                        'progress': (self.current_time - event_start) / (event_end - event_start)
                    }
        
        # Check for ended events
        for timeline_index, event in self.active_events.items():
            if timeline_index not in new_active_events:
                light_changes[timeline_index] = {
                    'event': event,
                    'action': 'end',
                    'progress': 1.0
                }
        
        # Update active events
        self.active_events = new_active_events
        
        # Call light change callback
        if light_changes and self.on_light_change:
            self.on_light_change(light_changes)
    
    def _time_to_seconds(self, time_str: str) -> float:
        """Převede čas string na sekundy."""
        try:
            parts = time_str.split(':')
            hours = int(parts[0])
            minutes = int(parts[1])
            
            sec_parts = parts[2].split('.')
            seconds = int(sec_parts[0])
            decimal = int(sec_parts[1]) / 10.0 if len(sec_parts) > 1 else 0.0
            
            return hours * 3600 + minutes * 60 + seconds + decimal
        except:
            return 0.0
    
    def get_playback_state(self) -> Dict:
        """Vrátí aktuální stav přehrávání."""
        return {
            'is_playing': self.is_playing,
            'current_time': self.current_time,
            'duration': self.duration,
            'progress': self.current_time / self.duration if self.duration > 0 else 0,
            'active_events_count': len(self.active_events),
            'active_events': list(self.active_events.values())
        }