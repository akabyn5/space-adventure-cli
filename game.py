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
"""

import sys
import time
from typing import List, Dict
from dataclasses import dataclass, field

# Game constants
VALID_CHOICES = {"1", "2"}
BORDER_WIDTH = 60
STORY_READ_DELAY = 1
ENDING_READ_DELAY = 1.5
TRANSITION_DELAY = 0.8
TITLE_DELAY = 1.5


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
    
    def add_points(self, points: int, description: str) -> None:
        """Add points to score with description."""
        self.score += points
        self.mission_log.append(f"[+{points}pts] {description}")
    
    def add_radiation(self, amount: int) -> None:
        """Increase radiation exposure."""
        self.radiation_level += amount
    
    def record_choice(self, decision_name: str, choice: str) -> None:
        """Record a decision made by the player."""
        self.choices_made[decision_name] = choice


def clear_screen() -> None:
    """Clear the console screen."""
    print("\n" * 2)


def display_title() -> None:
    """Display the game title and introduction with ASCII art."""
    print("=" * BORDER_WIDTH)
    print("""
    ███████╗██████╗  █████╗  ██████╗███████╗    █████╗ ██████╗ ██╗   ██╗███████╗███╗   ██╗████████╗██╗   ██╗██████╗ ███████╗
    ██╔════╝██╔══██╗██╔══██╗██╔════╝██╔════╝   ██╔══██╗██╔══██╗██║   ██║██╔════╝████╗  ██║╚══██╔══╝██║   ██║██╔══██╗██╔════╝
    ███████╗██████╔╝███████║██║     █████╗     ███████║██║  ██║██║   ██║█████╗  ██╔██╗ ██║   ██║   ██║   ██║██████╔╝█████╗
    ╚════██║██╔═══╝ ██╔══██║██║     ██╔══╝     ██╔══██║██║  ██║██║   ██║██╔══╝  ██║╚██╗██║   ██║   ██║   ██║██╔══██╗██╔══╝
    ███████║██║     ██║  ██║╚██████╗███████╗   ██║  ██║██████╔╝╚██████╔╝███████╗██║ ╚████║   ██║   ╚██████╔╝██║  ██║███████╗
    ╚══════╝╚═╝     ╚═╝  ╚═╝ ╚═════╝╚══════╝   ╚═╝  ╚═╝╚═════╝  ╚═════╝ ╚══════╝╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝╚══════╝
    """.center(BORDER_WIDTH))
    print("=" * BORDER_WIDTH)
    print("You are Commander Alex Chen, an elite astronaut.".center(BORDER_WIDTH))
    print("Mission: Recover the data core from the damaged station.".center(BORDER_WIDTH))
    print("=" * BORDER_WIDTH)
    print()
    time.sleep(TITLE_DELAY)


def get_valid_choice(prompt: str, valid_options: set) -> str:
    """
    Validate and return user input.
    
    Args:
        prompt: The question to display
        valid_options: Set of acceptable inputs
    
    Returns:
        The validated user choice
    """
    while True:
        choice = input(prompt).strip()
        if choice in valid_options:
            return choice
        print(f"❌ Invalid choice! Please enter one of: {', '.join(sorted(valid_options))}")


def display_game_status(state: GameState) -> None:
    """Display current mission stats during gameplay."""
    print(f"\n[MISSION STATUS] Score: {state.score} | Radiation: {state.radiation_level}%")
    if state.mission_log:
        print("[RECENT LOG]", state.mission_log[-1])
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
    print("▶ MISSION START: Station Omega ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
Your shuttle approaches the damaged research station. Alarms blare
from the station's emergency systems. The main docking bay is flooded
with radiation, but you detect an alternative airlock on the side.

As you prepare to dock, your AI companion alerts you:
"Commander, I'm detecting an explosion in the reactor core. We have
approximately 2 hours before critical meltdown. Choose your approach."
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Dock at the MAIN airlock (direct but dangerous - high radiation)")
    print("2) Use the SIDE airlock (safer route but longer path)\n")
    
    time.sleep(STORY_READ_DELAY)
    choice = get_valid_choice("Your choice (1 or 2): ", VALID_CHOICES)
    state.record_choice("approach_station", choice)
    
    if choice == "1":
        state.add_radiation(25)
        state.made_risky_choice = True
        state.add_points(5, "Bold approach via main airlock")
    else:
        state.add_radiation(10)
        state.add_points(10, "Cautious approach via side airlock")
    
    display_game_status(state)
    return choice


def decision_handle_crew_comms(state: GameState) -> str:
    """
    Decision 2A: Handle crew communications in main airlock path.
    
    Returns:
        "1" for rescue crew, "2" for eject core
    """
    clear_screen()
    print("▶ MAIN AIRLOCK APPROACH ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
You dock at the main airlock against all warnings. Your suit's
radiation shielding activates, but the Geiger counter clicks rapidly.

You move through the station quickly, passing the control room where
sparks fly from damaged consoles. Suddenly, an emergency door seals
behind you - the radiation levels spike CRITICALLY.

A crewmate's voice crackles through the comms: "Commander! I'm still
in the data storage room. I've secured the core, but the exit is
blocked by debris. I can hold onto the core and try to reach you, or
I can trigger an emergency compress capsule to eject it separately."
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Tell them to bring the core - you'll create an escape route")
    print("2) Have them eject the core - save the data at any cost\n")
    
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
    print("▶ SIDE AIRLOCK APPROACH ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
You carefully navigate to the side airlock. The entry is slower, but
your radiation levels stay within safe parameters. Good thinking.

Inside the station, you move through the hydroponics bay. The plants
are wilting without power. As you approach the data center, your suit's
thermal scanner detects unusual heat signatures behind a locked door.

Your AI warns: "Commander, there are two ways forward:
1) Bypass the security system (quick, risky - might trigger alarms)
2) Use the maintenance tunnel (slow, safe - but will waste precious time)"
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Bypass the security system (risky - spend 15 minutes)")
    print("2) Use the maintenance tunnel (safer - spend 45 minutes)\n")
    
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
    print("▶ DATA CORE SECURED ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
You and your crewmate successfully escape through the maintenance
corridor. The station's reactor is reaching critical mass, but you
have the data core in your possession.

Your crewmate gasps: "Commander, this core contains revolutionary
data! We could analyze it right here on the shuttle, or we could
get it to safety first."

The shuttle's systems show you have just enough time for one action
before the station's explosion forces you to evacuate the area.
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Analyze the core onboard - unlock its secrets now")
    print("2) Rush to escape - prioritize safety over analysis\n")
    
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
    print("▶ CORE EJECTION COMPLETE ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
The emergency capsule successfully ejects the data core into space.
Your sensors track it tumbling away from the station. The reactor
meltdown is accelerating - you have limited time.

Your AI companion reports: "Commander, the core is 500 meters away.
We can attempt retrieval with the shuttle's robotic arm, or you
could perform an EVA (Extra-Vehicular Activity) to retrieve it
manually. The robotic arm is safer but less precise in zero-G."
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Use the robotic arm - safer but technically challenging")
    print("2) EVA retrieval - direct but exposes you to radiation\n")
    
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
    print("▶ SECURITY BREACH DETECTED ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
Your security bypass triggers every alarm in the station! Red lights
flash and klaxons wail. Security drones activate and begin converging
on your position. Your AI companion shouts: "Multiple hostiles
approaching! We need to act fast!"

You have two options: engage the drones directly with your suit's
defensive systems, or attempt an emergency hack of the security
mainframe to disable them remotely.
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Fight the security drones - use suit weapons")
    print("2) Emergency hack - try to disable security remotely\n")
    
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
    print("▶ MAINTENANCE TUNNEL - TIME CRITICAL ◀".center(BORDER_WIDTH))
    print("-" * BORDER_WIDTH)
    print("""
The maintenance tunnel stretches ahead, but your progress is slowed
by collapsed sections and debris. Your crewmate's voice is urgent:
"Commander, reactor temperature is spiking! We're cutting it too
close!"

Up ahead, you see the data center entrance, but it's blocked by
a massive debris field. You could try to force your way through,
or call for immediate extraction from your shuttle.
    """)
    print("-" * BORDER_WIDTH)
    print("\n1) Push through the debris - reach the core at any cost")
    print("2) Call for extraction - abandon the core to save lives\n")
    
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
    """Display final mission statistics and achievements."""
    print("=" * BORDER_WIDTH)
    print("MISSION FINAL STATISTICS".center(BORDER_WIDTH))
    print("=" * BORDER_WIDTH)
    print(f"Final Score: {state.score} points")
    print(f"Radiation Exposure: {state.radiation_level}%")
    print(f"Data Core Status: {'RECOVERED' if state.data_recovered else 'LOST'}")
    print(f"Crew Status: {'SAVED' if state.crew_saved else 'LOST'}")
    print()
    
    # Award medals based on performance
    if state.score >= 100:
        print("🏅 MEDAL EARNED: LEGENDARY COMMANDER")
        print("   Exceptional performance and decision-making!")
    elif state.score >= 80:
        print("🥇 MEDAL EARNED: ELITE OPERATIVE")
        print("   Outstanding heroism and professionalism!")
    elif state.score >= 60:
        print("🥈 MEDAL EARNED: SKILLED COMMANDER")
        print("   Strong leadership and tactical awareness!")
    elif state.score >= 40:
        print("🥉 MEDAL EARNED: COMPETENT OFFICER")
        print("   Mission completed with acceptable performance!")
    else:
        print("⚠️  Mission completed with minimal success!")
    
    print()
    if state.mission_log:
        print("MISSION LOG HIGHLIGHTS:")
        for entry in state.mission_log[-3:]:
            print(f"  {entry}")
    print("=" * BORDER_WIDTH)


def ending_heroic_rescue(state: GameState) -> None:
    """SUCCESS ENDING: Player rescues both the data and crew member."""
    clear_screen()
    time.sleep(ENDING_READ_DELAY)
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "🎉 SUCCESS: THE HERO'S RETURN 🎉".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
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
    """)
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
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "💥 FAILURE: MISSION LOST 💥".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
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
    """)
    show_final_stats(state)
    print()


def ending_scientific_discovery(state: GameState) -> None:
    """SUCCESS ENDING: Analyze core onboard, make breakthrough discovery."""
    clear_screen()
    time.sleep(ENDING_READ_DELAY)
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "🔬 BREAKTHROUGH DISCOVERY 🔬".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
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
    """)
    show_final_stats(state)
    print()


def ending_heroic_escape(state: GameState) -> None:
    """SUCCESS ENDING: Rush to escape with core intact."""
    clear_screen()
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "🚀 HEROIC ESCAPE 🚀".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
You prioritize safety and engage full thrust. The shuttle rockets
away just as Station Omega erupts in a massive explosion. You and
your crewmate survive, and the data core is safely secured.

Though you didn't analyze it onboard, the core reaches Earth intact.
Scientists there unlock its secrets, saving countless lives.

Mission Status: ✓ DATA PRESERVED
                ✓ CREW MEMBER SAVED
                ✓ SAFE EXTRACTION

Your courage ensured humanity's future, even if you couldn't see it yourself.
    """)
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
    print("╔" + "=" * 58 + "╗".rjust(1))
    print("║" + "⚔️ COMBAT VICTORY ⚔️".center(58) + "║")
    print("╚" + "=" * 58 + "╝")
    print("""
You engage the security drones with your suit's defensive systems.
Laser fire illuminates the corridors as you systematically disable
each threat. Your combat training proves invaluable.

With the drones neutralized, you secure the data core and escape
before the station's destruction.

Mission Status: ✓ DATA RECOVERED
                ✓ HOSTILES NEUTRALIZED
                ✓ COMBAT SUCCESS

Military strategists study your tactics for decades!
    """)
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
    input("Press Enter to begin your mission...\n")
    
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
    print("\n" + "=" * BORDER_WIDTH)
    print("Thanks for playing SPACE ADVENTURE!".center(BORDER_WIDTH))
    print("=" * BORDER_WIDTH)
    
    time.sleep(TRANSITION_DELAY)
    # Validate play again choice
    while True:
        play_again = input("\nDo you want to play again? (yes/no): ").strip().lower()
        if play_again in ["yes", "y", "no", "n"]:
            break
        print("❌ Invalid choice! Please enter 'yes' or 'no'.")
    
    if play_again in ["yes", "y"]:
        clear_screen()
        time.sleep(0.5)
        play_game()
    else:
        print("\nGoodbye, Commander! May your next mission be successful. 🚀\n")
        time.sleep(1)


if __name__ == "__main__":
    try:
        play_game()
    except KeyboardInterrupt:
        print("\n\nMission aborted by commander. 🛑")
        sys.exit(0)
