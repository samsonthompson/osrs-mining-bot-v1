from typing import List, Tuple, Dict
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class RSBank:
    name: str
    location: str
    coordinates: Tuple[int, int]  # (x, y) coordinates
    members: bool
    features: List[str]  # e.g., ['deposit box', 'ge access', 'chest']

class RunescapeBankFinder:
    def __init__(self):
        # Common bank locations in RuneScape
        self.bank_locations: List[RSBank] = [
            RSBank("Grand Exchange", "Varrock", (3165, 3487), False, 
                  ["ge access", "chest", "deposit box"]),
            RSBank("Varrock West", "Varrock", (3185, 3441), False, 
                  ["chest", "deposit box"]),
            RSBank("Lumbridge", "Lumbridge Castle", (3208, 3220), False, 
                  ["chest"]),
            RSBank("Edgeville", "Edgeville", (3094, 3491), False, 
                  ["chest", "deposit box"]),
            RSBank("Al Kharid", "Al Kharid", (3269, 3167), False, 
                  ["chest", "deposit box"]),
            RSBank("Falador East", "Falador", (3012, 3355), False, 
                  ["chest"]),
            RSBank("Draynor", "Draynor Village", (3092, 3245), False, 
                  ["chest", "deposit box"])
        ]

    def calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Calculate Manhattan distance between two points in RS coordinates"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def find_nearest_bank(self, current_pos: Tuple[int, int], members_only: bool = False) -> Dict:
        """
        Find the nearest bank from current position
        Args:
            current_pos: Current (x, y) coordinates
            members_only: Include member-only banks
        Returns:
            Dict with nearest bank info and path details
        """
        try:
            nearest_bank = None
            min_distance = float('inf')

            for bank in self.bank_locations:
                if members_only and not bank.members:
                    continue

                distance = self.calculate_distance(current_pos, bank.coordinates)
                if distance < min_distance:
                    min_distance = distance
                    nearest_bank = bank

            if nearest_bank:
                return {
                    "bank": nearest_bank,
                    "distance": min_distance,
                    "estimated_time": self.estimate_walk_time(min_distance),
                    "path_description": self.get_path_description(current_pos, nearest_bank)
                }
            return None

        except Exception as e:
            logger.error(f"Error finding nearest bank: {str(e)}")
            return None

    def estimate_walk_time(self, distance: int) -> str:
        """Estimate walking time based on distance"""
        # Assuming average walking speed in RS
        seconds = distance * 0.6  # rough estimate
        if seconds < 60:
            return f"{int(seconds)} seconds"
        return f"{int(seconds/60)} minutes"

    def get_path_description(self, current_pos: Tuple[int, int], bank: RSBank) -> str:
        """Generate a simple path description to the bank"""
        x_diff = bank.coordinates[0] - current_pos[0]
        y_diff = bank.coordinates[1] - current_pos[1]
        
        directions = []
        if x_diff > 0:
            directions.append(f"East {abs(x_diff)} squares")
        elif x_diff < 0:
            directions.append(f"West {abs(x_diff)} squares")
            
        if y_diff > 0:
            directions.append(f"North {abs(y_diff)} squares")
        elif y_diff < 0:
            directions.append(f"South {abs(y_diff)} squares")

        return f"Head {' then '.join(directions)} to reach {bank.name} bank"

    def get_bank_features(self, bank_name: str) -> List[str]:
        """Get available features at specified bank"""
        for bank in self.bank_locations:
            if bank.name.lower() == bank_name.lower():
                return bank.features
        return []