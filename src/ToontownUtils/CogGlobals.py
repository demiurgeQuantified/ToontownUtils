from panda3d.core import Vec4

waiterLeg = "phase_3.5/maps/waiter_m_leg.png"
waiterBlazer = "phase_3.5/maps/waiter_m_blazer.png"
waiterSleeve = "phase_3.5/maps/waiter_m_sleeve.png"

healthMeterModel = "phase_3.5/models/gui/matching_game_gui.bam"
healthMeterGlowModel = "phase_3.5/models/props/glow.bam"

HealthColor: dict[str, Vec4] = {
    "green": Vec4(0, 1, 0, 1),
    "yellow": Vec4(1, 1, 0, 1),
    "orange": Vec4(1, 0.5, 0, 1),
    "red": Vec4(1, 0, 0, 1),
    "off": Vec4(0.3, 0.3, 0.3, 1),
}
HealthGlowColor: dict[str, Vec4] = {
    "green": Vec4(0.25, 1, 0.25, 0.5),
    "yellow": Vec4(1, 1, 0.25, 0.5),
    "orange": Vec4(1, 0.5, 0.25, 0.5),
    "red": Vec4(1, 0.25, 0.25, 0.5),
    "off": Vec4(0.3, 0.3, 0.3, 0),
}
