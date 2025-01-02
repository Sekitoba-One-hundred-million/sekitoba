def skip_key( key ):
    if "predict" in key \
      or "judgment" in key \
      or "true_skill" in key \
      or "speed_index" in key \
      or "up_rate" in key \
      or "stamina" in key \
      or "max_time_point" in key \
      or "max_up3_time_point" in key \
      or "level_score" in key \
      or "up_index" in key \
      or "pace_up" in key \
      or "level_up3" in key \
      or "_one" in key \
      or "_two" in key \
      or "_three" in key \
      or "before_race_score" in key \
      or "power" in key \
      or "kinetic_energy" in key \
      or key == "odds":
        return True

    return False
