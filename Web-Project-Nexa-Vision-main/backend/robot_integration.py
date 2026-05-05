# Robot Integration Service
# This module bridges the Web Dashboard with the Pipe Robot Project

import httpx
import os
from typing import Dict, List, Optional
from dotenv import load_dotenv
import logging

load_dotenv()

logger = logging.getLogger(__name__)

ROBOT_API_URL = os.getenv("ROBOT_API_URL", "http://localhost:8000")

class RobotClient:
    """Client to communicate with the Pipe Robot API"""
    
    def __init__(self, base_url: str = ROBOT_API_URL):
        self.base_url = base_url.rstrip("/")
        self.timeout = 10.0
    
    async def move(self, direction: str) -> Dict:
        """
        Control robot movement
        
        Args:
            direction: "forward", "backward", "left", "right", or "stop"
        
        Returns:
            Status response from robot
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/move",
                    json={"direction": direction},
                    timeout=self.timeout
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error sending move command to robot: {str(e)}")
            raise
    
    async def run_ai_detection(self) -> Dict:
        """
        Trigger AI detection on the robot
        
        Returns:
            Detection results
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/ai/run",
                    timeout=self.timeout
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error running AI detection: {str(e)}")
            raise
    
    async def get_distance(self) -> Dict:
        """
        Get distance from ultrasonic sensor
        
        Returns:
            Distance measurement
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/distance",
                    timeout=self.timeout
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error getting distance: {str(e)}")
            raise
    
    async def get_encoder_count(self) -> Dict:
        """
        Get encoder count
        
        Returns:
            Encoder count
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/encoder",
                    timeout=self.timeout
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error getting encoder count: {str(e)}")
            raise
    
    async def get_status(self) -> Dict:
        """
        Get current robot status
        
        Returns:
            Current command and detections
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"{self.base_url}/status",
                    timeout=self.timeout
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error getting robot status: {str(e)}")
            raise
    
    async def receive_detections(self, detections: List) -> Dict:
        """
        Send detections to robot
        
        Args:
            detections: List of detection results
        
        Returns:
            Confirmation response
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/detections",
                    json={"detections": detections},
                    timeout=self.timeout
                )
                return response.json()
        except Exception as e:
            logger.error(f"Error sending detections: {str(e)}")
            raise
    
    def get_video_stream_url(self) -> str:
        """Get the URL for video streaming"""
        return f"{self.base_url}/video"

# Singleton instance
robot_client = RobotClient()
