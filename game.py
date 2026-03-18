"""
SPACE ADVENTURE: A Choose Your Own Adventure Game
You are an astronaut on a critical mission to save humanity.
Your choices will determine your fate among the stars.

Game Structure:
- Decision functions present story branches and collect player choices
- Ending functions display the outcome based on accumulated choices
- Main game flow orchestrates the decision tree
- Input validation ensures only valid choices are accepted
- GameState tracks player progress, score, and radiation levels
- Mission log records all decisions made during gameplay
- Colors and sound effects enhance immersion
"""

import sys
import time
import os
from typing import List, Dict
from dataclasses import dataclass, field

try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False

# ANSI Color codes for terminal output
class Color:
    """ANSI color codes for terminal output."""
    CYAN = '\033[96m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    MAGENTA = '\033[95m'
    BLUE = '\033[94m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    BLINK = '\033[5m'
    REVERSE = '\033[7m'

# Game constants
VALID_CHOICES = {"1", "2"}
BORDER_WIDTH = 60
STORY_READ_DELAY = 0.8
ENDING_READ_DELAY = 1.2
TRANSITION_DELAY = 0.6
TITLE_DELAY = 1.2

# Sound effect frequencies and durations (Hz, ms)
ALERT_SOUND = (1000, 150)
SUCCESS_SOUND = (1500, 200)
WARNING_SOUND = (800, 300)
EXPLOSION_SOUND = (400, 500)
BEEP_SOUND = (600, 100)


def play_sound(frequency: int = 1000, duration: int = 100) -> None:
    """Cross-platform sound effect player."""
    if HAS_WINSOUND and sys.platform == "win32":
        try:
            winsound.Beep(frequency, duration)
        except Exception:
            pass


def play_alert() -> None:
    """Play alert sound."""
    play_sound(ALERT_SOUND[0], ALERT_SOUND[1])


def play_success() -> None:
    """Play success sound."""
    play_sound(SUCCESS_SOUND[0], SUCCESS_SOUND[1])
    time.sleep(0.1)
    play_sound(SUCCESS_SOUND[0], SUCCESS_SOUND[1])


def play_warning() -> None:
    """Play warning sound."""
    play_sound(WARNING_SOUND[0], WARNING_SOUND[1])


def play_beep() -> None:
    """Play simple beep sound."""
    play_sound(BEEP_SOUND[0], BEEP_SOUND[1])


def play_explosion() -> None:
    """Play explosion sound effect."""
    play_sound(EXPLOSION_SOUND[0], EXPLOSION_SOUND[1])


def colored(text: str, color: str) -> str:
    """Return colored text."""
    return f"{color}{text}{Color.RESET}"


def radar_scan(duration: float = 2) -> None:
    """Animate a radar scan effect."""
    print(colored("   SCANNING AREA...", Color.CYAN))
    frames = ["   ◜    ", "    ◝   ", "     ◞  ", "      ◟ ", "       ◞", "      ◜ ", "     ◝  ", "    ◞   ", "   ◟    "]
    end_time = time.time() + duration
    while time.time() < end_time:
        for frame in frames:
            print(colored(frame, Color.CYAN), end='\r')
            time.sleep(0.1)
    print(colored("   ✓ SCAN COMPLETE   ", Color.GREEN))


def loading_bar(label: str, duration: float = 1.5, width: int = 30) -> None:
    """Animate a loading bar."""
    print(colored(f"   {label}", Color.YELLOW))
    start_time = time.time()
    while time.time() - start_time < duration:
        progress = (time.time() - start_time) / duration
        filled = int(progress * width)
        bar = "█" * filled + "░" * (width - filled)
        percentage = int(progress * 100)
        print(colored(f"   [{bar}] {percentage}%", Color.YELLOW), end='\r')
        time.sleep(0.05)
    print(colored(f"   [{'█' * width}] 100%      ", Color.GREEN))


def alarm_animation(duration: float = 1.5) -> None:
    """Animate alarm activation."""
    play_alert()
    end_time = time.time() + duration
    alarm_chars = ["⚠", "⚠", " "]
    idx = 0
    while time.time() < end_time:
        print(colored(f"   {alarm_chars[idx % 3]} ALERT TRIGGERED {alarm_chars[idx % 3]}", Color.RED), end='\r')
        idx += 1
        time.sleep(0.15)
    print(colored("   ⚠ ALERT TRIGGERED ⚠     ", Color.RED))


def explosion_animation() -> None:
    """Animate explosion effect."""
    play_explosion()
    explosion_frames = [
        "    •",
        "   •••",
        "  •••••",
        " •••••••",
        "•••••••••",
        " •••••••",
        "  •••••",
        "   •••",
        "    •"
    ]
    for frame in explosion_frames:
        print(colored(frame, Color.RED + Color.BOLD), end='\r')
        time.sleep(0.1)
    print(colored("         ", Color.RED))  # Clear


def reactor_status_animation(pressure: int = 50) -> None:
    """Animate reactor status with increasing pressure."""
    print(colored("   REACTOR STATUS:", Color.YELLOW))
    for i in range(pressure):
        filled = int((i / 100) * 20)
        bar = "▥" * filled + "▤" * (20 - filled)
        temp = 2000 + (i * 20)
        color = Color.GREEN if i < 30 else Color.YELLOW if i < 70 else Color.RED
        print(colored(f"   [TEMP: {temp}K] {bar} {i}%", color), end='\r')
        time.sleep(0.03)
    print()


def shuttle_approach_animation() -> None:
    """Animate shuttle approaching station."""
    print(colored("   SHUTTLE APPROACH SEQUENCE:", Color.CYAN))
    frames = [
        "        🚀",
        "       🚀 ",
        "      🚀  ",
        "     🚀   ",
        "    🚀    ",
        "   🚀     ",
        "  🚀      ",
        " 🚀       ",
        "🚀 ███████"  # Station
    ]
    for frame in frames:
        print(colored(frame, Color.CYAN), end='\r')
        time.sleep(0.15)
    print(colored("✓ DOCKING SEQUENCE INITIATED", Color.GREEN))


def data_transfer_animation(duration: float = 1.2) -> None:
    """Animate data transfer progress."""
    print(colored("   TRANSFERRING DATA CORE...", Color.MAGENTA))
    start_time = time.time()
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    idx = 0
    while time.time() - start_time < duration:
        print(colored(f"   {frames[idx % len(frames)]} ENCRYPTING AND TRANSFERRING...", Color.MAGENTA), end='\r')
        idx += 1
        time.sleep(0.1)
    print(colored("   ✓ DATA CORE SECURED", Color.GREEN))


def status_bar(current: int, maximum: int, width: int = 20) -> str:
    """Create a visual status bar."""
    filled = int((current / maximum) * width)
    bar = "█" * filled + "░" * (width - filled)
    return f"[{bar}] {current}/{maximum}"


@dataclass
class GameState:
    """Tracks player progress, score, and game statistics."""
    score: int = 0
    radiation_level: int = 0
    crew_saved: bool = False
    data_recovered: bool = False
    made_risky_choice: bool = False
    mission_log: List[str] = field(default_factory=list)
    choices_made: Dict[str, str] = field(default_factory=dict)
    decision_count: int = 0
    
    def add_points(self, points: int, description: str) -> None:
        """Add points to score with description."""
        self.score += points
        self.mission_log.append(f"{colored(f'[+{points}pts]', Color.GREEN)} {description}")
    
    def add_radiation(self, amount: int) -> None:
        """Increase radiation exposure."""
        self.radiation_level = min(100, self.radiation_level + amount)
    
    def record_choice(self, decision_name: str, choice: str) -> None:
        """Record a decision made by the player."""
        self.choices_made[decision_name] = choice
        self.decision_count += 1


def clear_screen() -> None:
    """Clear the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


def display_title() -> None:
    """Display the game title and introduction with ASCII art and colors."""
    play_success()
    clear_screen()
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    print(f"""{Color.BOLD}{Color.CYAN}
    ███████╗██████╗  █████╗  ██████╗███████╗    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
    ███████╗██████╔╝███████║██║     █████╗     ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗
    ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝     ██╔══██║██║  ██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝
    ███████║██║     ██║  ██║╚██████╗███████╗   ██║  ██║██████╔╝╚██████╔╝███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗
    ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝   ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
    {Color.RESET}""".center(BORDER_WIDTH))
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    print(colored("You are Commander Alex Chen, an elite astronaut.".center(BORDER_WIDTH), Color.YELLOW))
    print(colored("Mission: Recover the data core from the damaged station.".center(BORDER_WIDTH), Color.YELLOW))
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    print()
    time.sleep(TITLE_DELAY)


def get_valid_choice(prompt: str, valid_options: set) -> str:
    """
    Validate and return user input with colored feedback.
    
    Args:
        prompt: The question to display
        valid_options: Set of acceptable inputs
    
    Returns:
        The validated user choice
    """
    while True:
        choice = input(colored(prompt, Color.BOLD + Color.CYAN)).strip()
        if choice in valid_options:
            play_beep()
            return choice
        play_warning()
        print(colored(f"❌ Invalid choice! Please enter one of: {', '.join(sorted(valid_options))}", Color.RED))


def display_game_status(state: GameState) -> None:
    """Display current mission stats during gameplay with colors and status bars."""
    radiation_color = Color.GREEN if state.radiation_level < 50 else Color.YELLOW if state.radiation_level < 80 else Color.RED
    
    print(f"\n{Color.BOLD}{Color.CYAN}[MISSION STATUS]{Color.RESET}")
    print(f"  Score: {colored(str(state.score), Color.GREEN)} | Radiation: {colored(status_bar(state.radiation_level, 100), radiation_color)}")
    print(f"  Decisions: {colored(str(state.decision_count), Color.CYAN)}/4")
    
    if state.mission_log:
        log_entry = state.mission_log[-1]
        print(f"  {colored('Recent:', Color.MAGENTA)} {log_entry}")
    print()


def decision_approach_station(state: GameState) -> str:
    """
    First major decision point: Choose initial approach to the station.
    
    Presents the player with two options:
    1. Main airlock (dangerous but direct)
    2. Side airlock (safer but slower)
    
    Returns:
        "1" for main airlock, "2" for side airlock
    """
    clear_screen()
    play_alert()
    shuttle_approach_animation()
    print()
    print(colored("▶ MISSION START: Station Omega ◀".center(BORDER_WIDTH), Color.BOLD + Color.CYAN))
    print(f"{Color.CYAN}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
Your shuttle approaches the damaged research station. Alarms blare
from the station's emergency systems. The main docking bay is flooded
with radiation, but you detect an alternative airlock on the side.

As you prepare to dock, your AI companion alerts you:
"Commander, I'm detecting an explosion in the reactor core. We have
approximately 2 hours before critical meltdown. Choose your approach."
    """, Color.YELLOW))
    print(f"{Color.CYAN}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    radar_scan(1.5)
    print()
    
    print(f"\n{Color.RED}1) Dock at the MAIN airlock (direct but dangerous - high radiation){Color.RESET}")
    print(f"{Color.GREEN}2) Use the SIDE airlock (safer route but longer path){Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("approach_station", choice)
    
    if choice == "1":
        play_warning()
        alarm_animation(1)
        print()
        state.add_radiation(25)
        state.made_risky_choice = True
        state.add_points(5, "Bold approach via main airlock")
        print(colored("⚠️  HIGH RADIATION DETECTED", Color.RED))
    else:
        play_beep()
        loading_bar("Plotting safe route...", 0.8)
        print()
        state.add_radiation(10)
        state.add_points(10, "Cautious approach via side airlock")
        print(colored("✓ Safe passage route selected", Color.GREEN))
    
    display_game_status(state)
    return choice


def decision_handle_crew_comms(state: GameState) -> str:
    """
    Decision 2A: Handle crew communications in main airlock path.
    
    Returns:
        "1" for rescue crew, "2" for eject core
    """
    clear_screen()
    loading_bar("Initializing airlock sequence...", 1.2)
    print()
    print(colored("▶ MAIN AIRLOCK APPROACH ◀".center(BORDER_WIDTH), Color.BOLD + Color.RED))
    print(f"{Color.RED}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
You dock at the main airlock against all warnings. Your suit's
radiation shielding activates, but the Geiger counter clicks rapidly.

You move through the station quickly, passing the control room where
sparks fly from damaged consoles. Suddenly, an emergency door seals
behind you - the radiation levels spike CRITICALLY.

A crewmate's voice crackles through the comms: "Commander! I'm still
in the data storage room. I've secured the core, but the exit is
blocked by debris. I can hold onto the core and try to reach you, or
I can trigger an emergency compress capsule to eject it separately."
    """, Color.YELLOW))
    print(f"{Color.RED}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    reactor_status_animation(65)
    print()
    
    print(f"\n{Color.GREEN}1) Tell them to bring the core - you'll create an escape route")
    print(f"{Color.YELLOW}2) Have them eject the core - save the data at any cost{Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("crew_comms", choice)
    
    if choice == "1":
        play_success()
        data_transfer_animation()
        state.crew_saved = True
        state.add_points(15, "Chose to rescue crew member")
        state.add_radiation(15)
    else:
        play_alert()
        loading_bar("Ejecting data core...", 1)
        state.data_recovered = True
        state.add_points(10, "Prioritized data core ejection")
        state.add_radiation(5)
    
    display_game_status(state)
    return choice
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("crew_comms", choice)
    
    if choice == "1":
        state.crew_saved = True
        state.add_points(15, "Chose to rescue crew member")
        state.add_radiation(15)
    else:
        state.data_recovered = True
        state.add_points(10, "Prioritized data core ejection")
        state.add_radiation(5)
    
    display_game_status(state)
    return choice


def decision_security_bypass(state: GameState) -> str:
    """
    Decision 2B: Choose security approach in side airlock path.
    
    Returns:
        "1" for bypass security, "2" for maintenance tunnel
    """
    clear_screen()
    radar_scan(1.5)
    print()
    print(colored("▶ SIDE AIRLOCK APPROACH ◀".center(BORDER_WIDTH), Color.BOLD + Color.GREEN))
    print(f"{Color.GREEN}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
You carefully navigate to the side airlock. The entry is slower, but
your radiation levels stay within safe parameters. Good thinking.

Inside the station, you move through the hydroponics bay. The plants
are wilting without power. As you approach the data center, your suit's
thermal scanner detects unusual heat signatures behind a locked door.

Your AI warns: "Commander, there are two ways forward:
1) Bypass the security system (quick, risky - might trigger alarms)
2) Use the maintenance tunnel (slow, safe - but will waste precious time)"
    """, Color.YELLOW))
    print(f"{Color.GREEN}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    loading_bar("Scanning security protocols...", 1)
    print()
    
    print(f"\n{Color.RED}1) Bypass the security system (risky - spend 15 minutes)")
    print(f"{Color.GREEN}2) Use the maintenance tunnel (safer - spend 45 minutes){Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("security_bypass", choice)
    
    if choice == "1":
        loading_bar("Bypassing security...", 1)
        print()
        state.made_risky_choice = True
        state.add_points(8, "Risky security bypass attempt")
        state.add_radiation(12)
    else:
        loading_bar("Navigating tunnel...", 1.2)
        print()
        state.add_points(12, "Chose safer maintenance tunnel")
        state.add_radiation(5)
    
    display_game_status(state)
    return choice
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("security_bypass", choice)
    
    if choice == "1":
        state.made_risky_choice = True
        state.add_points(8, "Risky security bypass attempt")
        state.add_radiation(12)
    else:
        state.add_points(12, "Chose safer maintenance tunnel")
        state.add_radiation(5)
    
    display_game_status(state)
    return choice


def decision_data_core_action(state: GameState) -> str:
    """
    Decision 3A: What to do with the rescued data core.
    
    Returns:
        "1" for analyze onboard, "2" for rush to escape
    """
    clear_screen()
    data_transfer_animation()
    print()
    print(colored("▶ DATA CORE SECURED ◀".center(BORDER_WIDTH), Color.BOLD + Color.MAGENTA))
    print(f"{Color.MAGENTA}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
You and your crewmate successfully escape through the maintenance
corridor. The station's reactor is reaching critical mass, but you
have the data core in your possession.

Your crewmate gasps: "Commander, this core contains revolutionary
data! We could analyze it right here on the shuttle, or we could
get it to safety first."

The shuttle's systems show you have just enough time for one action
before the station's explosion forces you to evacuate the area.
    """, Color.YELLOW))
    print(f"{Color.MAGENTA}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    reactor_status_animation(85)
    print()
    
    print(f"\n{Color.MAGENTA}1) Analyze the core onboard - unlock its secrets now")
    print(f"{Color.CYAN}2) Rush to escape - prioritize safety over analysis{Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("core_action", choice)
    
    if choice == "1":
        loading_bar("Analyzing data core...", 1.2)
        print()
        state.add_points(20, "Analyzed data core for scientific breakthrough")
        state.add_radiation(8)
    else:
        play_success()
        print(colored("   ✓ FULL THROTTLE ENGAGED", Color.GREEN))
        state.add_points(15, "Prioritized escape and data preservation")
        state.add_radiation(2)
    
    state.data_recovered = True
    display_game_status(state)
    return choice
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("core_action", choice)
    
    if choice == "1":
        state.add_points(20, "Analyzed data core for scientific breakthrough")
        state.add_radiation(8)
    else:
        state.add_points(15, "Prioritized escape and data preservation")
        state.add_radiation(2)
    
    state.data_recovered = True
    display_game_status(state)
    return choice


def decision_core_retrieval(state: GameState) -> str:
    """
    Decision 3B: How to retrieve the ejected data core.
    
    Returns:
        "1" for robotic arm, "2" for EVA
    """
    clear_screen()
    radar_scan(1.8)
    print()
    print(colored("▶ CORE EJECTION COMPLETE ◀".center(BORDER_WIDTH), Color.BOLD + Color.BLUE))
    print(f"{Color.BLUE}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
The emergency capsule successfully ejects the data core into space.
Your sensors track it tumbling away from the station. The reactor
meltdown is accelerating - you have limited time.

Your AI companion reports: "Commander, the core is 500 meters away.
We can attempt retrieval with the shuttle's robotic arm, or you
could perform an EVA (Extra-Vehicular Activity) to retrieve it
manually. The robotic arm is safer but less precise in zero-G."
    """, Color.YELLOW))
    print(f"{Color.BLUE}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    loading_bar("Calculating retrieval options...", 1)
    print()
    
    print(f"\n{Color.BLUE}1) Use the robotic arm - safer but technically challenging")
    print(f"{Color.YELLOW}2) EVA retrieval - direct but exposes you to radiation{Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("core_retrieval", choice)
    
    if choice == "1":
        loading_bar("Maneuvering robotic arm...", 1.2)
        print()
        state.add_points(18, "Successfully retrieved core with robotic arm")
        state.add_radiation(3)
    else:
        play_alert()
        alarm_animation(1)
        print()
        state.add_points(12, "Performed dangerous EVA retrieval")
        state.add_radiation(30)
    
    state.data_recovered = True
    display_game_status(state)
    return choice
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("core_retrieval", choice)
    
    if choice == "1":
        state.add_points(18, "Successfully retrieved core with robotic arm")
        state.add_radiation(3)
    else:
        state.add_points(12, "Performed dangerous EVA retrieval")
        state.add_radiation(30)
    
    state.data_recovered = True
    display_game_status(state)
    return choice


def decision_alarm_response(state: GameState) -> str:
    """
    Decision 3C: How to respond to triggered security alarms.
    
    Returns:
        "1" for fight drones, "2" for emergency hack
    """
    clear_screen()
    alarm_animation(2)
    print()
    print(colored("▶ SECURITY BREACH DETECTED ◀".center(BORDER_WIDTH), Color.BOLD + Color.RED))
    print(f"{Color.RED}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
Your security bypass triggers every alarm in the station! Red lights
flash and klaxons wail. Security drones activate and begin converging
on your position. Your AI companion shouts: "Multiple hostiles
approaching! We need to act fast!"

You have two options: engage the drones directly with your suit's
defensive systems, or attempt an emergency hack of the security
mainframe to disable them remotely.
    """, Color.YELLOW))
    print(f"{Color.RED}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    print(colored("   ⚠ DETECTING 3 SECURITY DRONES", Color.RED))
    print(colored("   ⚠ WEAPONS SYSTEMS ARMED", Color.RED))
    print(colored("   ⚠ TIME UNTIL INTERCEPT: 45 SECONDS", Color.RED))
    print()
    
    print(f"\n{Color.RED}1) Fight the security drones - use suit weapons")
    print(f"{Color.MAGENTA}2) Emergency hack - try to disable security remotely{Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("alarm_response", choice)
    
    if choice == "1":
        play_alert()
        print(colored("   ⬛⬜⬜ ENGAGING COMBAT MODE ⬜⬜⬛", Color.RED))
        loading_bar("Targeting drones...", 1)
        print()
        state.add_points(14, "Defeated security drones in combat")
        state.add_radiation(10)
    else:
        loading_bar("Executing emergency hack...", 1.2)
        print()
        state.add_points(8, "Attempted emergency security hack")
        state.add_radiation(5)
    
    display_game_status(state)
    return choice
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("alarm_response", choice)
    
    if choice == "1":
        state.add_points(14, "Defeated security drones in combat")
        state.add_radiation(10)
    else:
        state.add_points(8, "Attempted emergency security hack")
        state.add_radiation(5)
    
    display_game_status(state)
    return choice


def decision_tunnel_pressure(state: GameState) -> str:
    """
    Decision 3D: How to handle time pressure in the maintenance tunnel.
    
    Returns:
        "1" for push through debris, "2" for call extraction
    """
    clear_screen()
    reactor_status_animation(90)
    print()
    print(colored("▶ MAINTENANCE TUNNEL - TIME CRITICAL ◀".center(BORDER_WIDTH), Color.BOLD + Color.RED))
    print(f"{Color.RED}{'-' * BORDER_WIDTH}{Color.RESET}")
    print(colored("""
The maintenance tunnel stretches ahead, but your progress is slowed
by collapsed sections and debris. Your crewmate's voice is urgent:
"Commander, reactor temperature is spiking! We're cutting it too
close!"

Up ahead, you see the data center entrance, but it's blocked by
a massive debris field. You could try to force your way through,
or call for immediate extraction from your shuttle.
    """, Color.YELLOW))
    print(f"{Color.RED}{'-' * BORDER_WIDTH}{Color.RESET}")
    
    play_warning()
    alarm_animation(1.2)
    print()
    
    print(f"\n{Color.RED}1) Push through the debris - reach the core at any cost")
    print(f"{Color.GREEN}2) Call for extraction - abandon the core to save lives{Color.RESET}\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("tunnel_pressure", choice)
    
    if choice == "1":
        loading_bar("Pushing through debris field...", 1.2)
        print()
        state.made_risky_choice = True
        state.add_points(10, "Risked everything to push through debris")
        state.add_radiation(20)
    else:
        loading_bar("Calling shuttle for extraction...", 1)
        print()
        state.add_points(16, "Made tough call to prioritize crew survival")
        state.crew_saved = True
    
    display_game_status(state)
    return choice
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("tunnel_pressure", choice)
    
    if choice == "1":
        state.made_risky_choice = True
        state.add_points(10, "Risked everything to push through debris")
        state.add_radiation(20)
    else:
        state.add_points(16, "Made tough call to prioritize crew survival")
        state.crew_saved = True
    
    display_game_status(state)
    return choice


def show_final_stats(state: GameState) -> None:
    """Display final mission statistics and achievements with colors."""
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    print(colored("MISSION FINAL STATISTICS".center(BORDER_WIDTH), Color.BOLD + Color.CYAN))
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    
    score_color = Color.GREEN if state.score >= 80 else Color.YELLOW if state.score >= 60 else Color.RED
    radiation_color = Color.GREEN if state.radiation_level <= 30 else Color.YELLOW if state.radiation_level <= 70 else Color.RED
    
    print(f"Final Score: {colored(str(state.score), score_color)} points")
    print(f"Radiation Exposure: {colored(status_bar(state.radiation_level, 100), radiation_color)}")
    print(f"Data Core Status: {colored('RECOVERED ✓', Color.GREEN if state.data_recovered else Color.RED)}")
    print(f"Crew Status: {colored('SAVED ✓', Color.GREEN if state.crew_saved else Color.RED)}")
    print()
    
    # Award medals based on performance
    if state.score >= 100:
        play_success()
        print(colored("🏅 MEDAL EARNED: LEGENDARY COMMANDER", Color.BOLD + Color.YELLOW))
        print(colored("   Exceptional performance and decision-making!", Color.YELLOW))
    elif state.score >= 80:
        play_success()
        print(colored("🥇 MEDAL EARNED: ELITE OPERATIVE", Color.BOLD + Color.CYAN))
        print(colored("   Outstanding heroism and professionalism!", Color.CYAN))
    elif state.score >= 60:
        play_beep()
        print(colored("🥈 MEDAL EARNED: SKILLED COMMANDER", Color.BOLD + Color.BLUE))
        print(colored("   Strong leadership and tactical awareness!", Color.BLUE))
    elif state.score >= 40:
        play_beep()
        print(colored("🥉 MEDAL EARNED: COMPETENT OFFICER", Color.BOLD + Color.WHITE))
        print(colored("   Mission completed with acceptable performance!", Color.WHITE))
    else:
        print(colored("⚠️  Mission completed with minimal success!", Color.YELLOW))
    
    print()
    if state.mission_log:
        print(colored("MISSION LOG HIGHLIGHTS:", Color.BOLD + Color.MAGENTA))
        for entry in state.mission_log[-3:]:
            print(f"  {entry}")
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")


def ending_heroic_rescue(state: GameState) -> None:
    """SUCCESS ENDING: Player rescues both the data and crew member."""
    clear_screen()
    play_success()
    time.sleep(ENDING_READ_DELAY)
    print(f"{Color.GREEN}╔{'=' * 58}╗{Color.RESET}".rjust(1))
    print(f"{Color.GREEN}║{colored('🎉 SUCCESS: THE HERO\'S RETURN 🎉', Color.BOLD).center(58)}║{Color.RESET}")
    print(f"{Color.GREEN}╚{'=' * 58}╝{Color.RESET}".rjust(1))
    print(colored("""
You and your crewmate escape through the maintenance corridor just
as the reactor reaches critical levels. The station explodes in a
brilliant flash behind you as you dock your shuttle.

Back on Earth, you're celebrated as a hero. The data core contains
the cure for a mysterious disease affecting millions. Thousands of
lives are saved because of your courage and quick thinking.

Mission Status: ✓ DATA RECOVERED
                ✓ CREW MEMBER SAVED
                ✓ HUMANITY SAVED

Commander Chen, your legend lives on in the stars! 🌟
    """, Color.GREEN))
    show_final_stats(state)
    print()


def ending_data_saved(state: GameState) -> None:
    """NEUTRAL ENDING: Data saved but at a cost."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "⚠️ NEUTRAL ENDING: MISSION COMPLETE ⚠️".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
The emergency capsule ejects the data core as the station begins its
final decay. Your crewmate tries to make it back but is caught in a
secondary explosion. The data core shoots into space, and you manage
to retrieve it with your shuttle's robotic arm.

The mission is complete, but the cost was high. Your crewmate's
sacrifice is recorded in the mission logs. The data safely reaches
Earth and helps advance humanity's understanding of the cosmos.

Mission Status: ✓ DATA RECOVERED
                ✗ CREW MEMBER LOST
                ✓ MISSION COMPLETE

You carry the weight of this loss, but you know it served a greater good.
    """)
    show_final_stats(state)
    print()


def ending_catastrophic_failure(state: GameState) -> None:
    """FAILURE ENDING: Everything goes wrong."""
    clear_screen()
    play_explosion()
    print(f"{Color.RED}╔{'=' * 58}╗{Color.RESET}".rjust(1))
    print(f"{Color.RED}║{colored('💥 FAILURE: MISSION LOST 💥', Color.BOLD).center(58)}║{Color.RESET}")
    print(f"{Color.RED}╚{'=' * 58}╝{Color.RESET}".rjust(1))
    print(colored("""
The alarms you triggered alert the station's systems to your presence.
In panic, the automated defense systems seal all exits. You're trapped
inside as radiation levels skyrocket.

Your crewmate's final words echo through your comms: "I'm sorry,
Commander. We tried..." 

The backup power fails. Your shuttle is too far away. As the reactor
reaches critical mass, you realize your miscalculation has doomed you
both. Station Omega explodes in a brilliant flash.

The data core is lost forever.

Mission Status: ✗ DATA NOT RECOVERED
                ✗ CREW MEMBER LOST
                ✗ MISSION FAILED

Your sacrifice will be remembered, but humanity remains in darkness.
    """, Color.RED))
    show_final_stats(state)
    print()


def ending_scientific_discovery(state: GameState) -> None:
    """SUCCESS ENDING: Analyze core onboard, make breakthrough discovery."""
    clear_screen()
    play_success()
    time.sleep(ENDING_READ_DELAY)
    print(f"{Color.MAGENTA}╔{'=' * 58}╗{Color.RESET}".rjust(1))
    print(f"{Color.MAGENTA}║{colored('🔬 BREAKTHROUGH DISCOVERY 🔬', Color.BOLD).center(58)}║{Color.RESET}")
    print(f"{Color.MAGENTA}╚{'=' * 58}╝{Color.RESET}".rjust(1))
    print(colored("""
Against all odds, you activate the shuttle's analysis suite and
begin decoding the data core. As the station explodes behind you,
incredible discoveries unfold on your screens!

The core contains not just a cure for disease, but the blueprint
for unlimited clean energy. Your quick thinking saves humanity
from both medical and energy crises.

Mission Status: ✓ DATA ANALYZED
                ✓ CREW MEMBER SAVED
                ✓ SCIENTIFIC BREAKTHROUGH

You're remembered as the scientist who changed the course of human history!
    """, Color.MAGENTA))
    show_final_stats(state)
    print()


def ending_heroic_escape(state: GameState) -> None:
    """SUCCESS ENDING: Rush to escape with core intact."""
    clear_screen()
    play_success()
    print(f"{Color.CYAN}╔{'=' * 58}╗{Color.RESET}".rjust(1))
    print(f"{Color.CYAN}║{colored('🚀 HEROIC ESCAPE 🚀', Color.BOLD).center(58)}║{Color.RESET}")
    print(f"{Color.CYAN}╚{'=' * 58}╝{Color.RESET}".rjust(1))
    print(colored("""
You prioritize safety and engage full thrust. The shuttle rockets
away just as Station Omega erupts in a massive explosion. You and
your crewmate survive, and the data core is safely secured.

Though you didn't analyze it onboard, the core reaches Earth intact.
Scientists there unlock its secrets, saving countless lives.

Mission Status: ✓ DATA PRESERVED
                ✓ CREW MEMBER SAVED
                ✓ SAFE EXTRACTION

Your courage ensured humanity's future, even if you couldn't see it yourself.
    """, Color.CYAN))
    show_final_stats(state)
    print()


def ending_technical_mastery(state: GameState) -> None:
    """SUCCESS ENDING: Successfully retrieve core with robotic arm."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "🤖 TECHNICAL MASTERY 🤖".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
With expert precision, you maneuver the robotic arm through the
debris field. The delicate manipulators gently grasp the tumbling
data core and bring it safely aboard.

Your technical skill saves the mission. The core's data proves
vital for humanity's advancement in multiple fields.

Mission Status: ✓ DATA RECOVERED
                ✓ ROBOTIC RETRIEVAL SUCCESS
                ✓ MISSION COMPLETE

Engineers study your techniques for years to come!
    """)
    show_final_stats(state)
    print()


def ending_radiation_sacrifice(state: GameState) -> None:
    """NEUTRAL ENDING: EVA retrieval succeeds but at personal cost."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "☢️ RADIATION EXPOSURE ☢️".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
You spacewalk to retrieve the core manually. The EVA is successful,
but the radiation from the dying station batters your suit. You
return with the core, but your health is compromised.

The data is saved, but you pay a heavy personal price. Medical
treatment awaits you on Earth.

Mission Status: ✓ DATA RECOVERED
                ✓ EVA SUCCESS
                ⚠️ PERSONAL SACRIFICE

Your dedication inspires generations of astronauts.
    """)
    show_final_stats(state)
    print()


def ending_combat_victory(state: GameState) -> None:
    """SUCCESS ENDING: Fight and defeat security drones."""
    clear_screen()
    play_success()
    print(f"{Color.YELLOW}╔{'=' * 58}╗{Color.RESET}".rjust(1))
    print(f"{Color.YELLOW}║{colored('⚔️ COMBAT VICTORY ⚔️', Color.BOLD).center(58)}║{Color.RESET}")
    print(f"{Color.YELLOW}╚{'=' * 58}╝{Color.RESET}".rjust(1))
    print(colored("""
You engage the security drones with your suit's defensive systems.
Laser fire illuminates the corridors as you systematically disable
each threat. Your combat training proves invaluable.

With the drones neutralized, you secure the data core and escape
before the station's destruction.

Mission Status: ✓ DATA RECOVERED
                ✓ HOSTILES NEUTRALIZED
                ✓ COMBAT SUCCESS

Military strategists study your tactics for decades!
    """, Color.YELLOW))
    show_final_stats(state)
    print()


def ending_system_overload(state: GameState) -> None:
    """FAILURE ENDING: Emergency hack causes system overload."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "💻 SYSTEM OVERLOAD 💻".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
Your emergency hack attempt triggers a cascading system failure.
The station's AI goes rogue, sealing all exits and accelerating
the reactor meltdown. You're trapped as systems fail around you.

The data core is lost in the chaos, and Station Omega becomes
a warning beacon in space.

Mission Status: ✗ DATA LOST
                ✗ SYSTEMS COMPROMISED
                ✗ MISSION FAILED

Your attempt to save the situation only made it worse.
    """)
    show_final_stats(state)
    print()


def ending_tunnel_collapse(state: GameState) -> None:
    """FAILURE ENDING: Tunnel collapses during debris push."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "⛑️ TUNNEL COLLAPSE ⛑️".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
You force your way through the debris, but the structural damage
is too severe. The tunnel collapses around you, burying you and
your crewmate under tons of wreckage.

The reactor's final explosion echoes through the void. Station
Omega is gone, taking its secrets with it.

Mission Status: ✗ DATA NOT RECOVERED
                ✗ CREW LOST
                ✗ STRUCTURAL FAILURE

Sometimes pushing too hard leads to disaster.
    """)
    show_final_stats(state)
    print()


def ending_rescue_arrival(state: GameState) -> None:
    """NEUTRAL ENDING: Call for extraction, rescue team arrives."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "🛟 RESCUE ARRIVAL 🛟".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
You call for immediate extraction. A rescue shuttle arrives just
in time, pulling you and your crewmate to safety. The station
explodes moments later, but you survive.

The data core is lost, but lives are saved. Future missions will
learn from this experience.

Mission Status: ✗ DATA LOST
                ✓ CREW SAVED
                ✓ SAFE EXTRACTION

Sometimes the right choice is knowing when to retreat.
    """)
    show_final_stats(state)
    print()


def play_game() -> None:
    """
    Main game controller that orchestrates the entire adventure.
    
    Game Flow:
    1. Display title and introduction
    2. Initialize game state with tracking
    3. Present first decision (approach station)
    4. Branch based on choice:
       - Main airlock → crew rescue decision → core action decision
       - Side airlock → security decision → alarm response or tunnel pressure
    5. Display appropriate ending based on all choices
    6. Show final statistics and achievements
    7. Offer replay option
    """
    display_title()
    time.sleep(TRANSITION_DELAY)
    input(colored("Press Enter to begin your mission...\n", Color.BOLD + Color.YELLOW))
    
    # Initialize game state
    state = GameState()
    state.add_points(0, "Mission initiated")
    
    # Decision 1: Approach the station
    approach_choice = decision_approach_station(state)
    
    if approach_choice == "1":
        # Main airlock path - Decision 2A: Handle crew communications
        crew_choice = decision_handle_crew_comms(state)
        if crew_choice == "1":
            # Decision 3A: What to do with rescued data core
            core_action = decision_data_core_action(state)
            if core_action == "1":
                ending_scientific_discovery(state)
            else:
                ending_heroic_escape(state)
        else:
            # Decision 3B: How to retrieve ejected core
            retrieval_choice = decision_core_retrieval(state)
            if retrieval_choice == "1":
                ending_technical_mastery(state)
            else:
                ending_radiation_sacrifice(state)
    else:
        # Side airlock path - Decision 2B: Security bypass choice
        security_choice = decision_security_bypass(state)
        if security_choice == "1":
            # Decision 3C: Handle triggered alarms
            alarm_response = decision_alarm_response(state)
            if alarm_response == "1":
                ending_combat_victory(state)
            else:
                ending_system_overload(state)
        else:
            # Decision 3D: Time pressure in tunnel
            tunnel_choice = decision_tunnel_pressure(state)
            if tunnel_choice == "1":
                ending_tunnel_collapse(state)
            else:
                ending_rescue_arrival(state)
    
    time.sleep(2)
    print(f"\n{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    print(colored("Thanks for playing SPACE ADVENTURE!".center(BORDER_WIDTH), Color.BOLD + Color.CYAN))
    print(f"{Color.CYAN}{'=' * BORDER_WIDTH}{Color.RESET}")
    
    time.sleep(TRANSITION_DELAY)
    # Validate play again choice
    while True:
        play_again = input(colored("\nDo you want to play again? (yes/no): ", Color.BOLD + Color.YELLOW)).strip().lower()
        if play_again in ["yes", "y", "no", "n"]:
            break
        play_warning()
        print(colored("❌ Invalid choice! Please enter 'yes' or 'no'.", Color.RED))
    
    if play_again in ["yes", "y"]:
        clear_screen()
        time.sleep(0.5)
        play_game()
    else:
        print(colored("\nGoodbye, Commander! May your next mission be successful. 🚀\n", Color.BOLD + Color.CYAN))
        time.sleep(1)


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nMission aborted by commander. 🛑")
        sys.exit(0)
