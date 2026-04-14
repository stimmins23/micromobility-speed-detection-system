from src.database import create_table
from src.violation_handler import handle_speed_violation

create_table()

event = handle_speed_violation(18.7, location="Bench Test")

print(event)