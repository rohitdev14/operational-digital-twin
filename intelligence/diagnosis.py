"""Transparent evidence scoring for Day-3 hypotheses. No LLM and no ground-truth labels."""

def diagnose(e):
    hypotheses=[]
    vib_rise=e["vibration_delta_mm_s"]>=1.0
    load_rise=e["load_index_delta"]>=0.15
    overload=e["trip_code"]=="VSD_OVERLOAD"
    electrical_trip=e["trip_code"]=="ELECTRICAL_FAULT"

    mech_score=sum([vib_rise,load_rise,overload])
    # Absence of vibration can support an electrical path only when positive
    # electrical evidence also exists; absence alone must never create a cause.
    electrical_positive=electric_trip_or_load = electrical_trip or load_rise
    elec_score=(int(electrical_trip)+int(load_rise)+int(not vib_rise)) if electrical_positive else 0
    if mech_score:
        hypotheses.append({"hypothesis":"mechanical_load_or_bearing_degradation","score":mech_score,
          "supports":[x for x,b in [("vibration increased before trip",vib_rise),("electrical load increased",load_rise),("VSD overload trip recorded",overload)] if b],
          "missing":["bearing temperature","vibration spectrum","phase current measurements"]})
    if elec_score:
        hypotheses.append({"hypothesis":"electrical_supply_or_cable_fault","score":elec_score,
          "supports":[x for x,b in [("electrical fault trip recorded",electrical_trip),("electrical load excursion",load_rise),("no material vibration rise",not vib_rise)] if b],
          "missing":["phase current measurements","voltage imbalance","insulation/earth-fault evidence"]})
    hypotheses.sort(key=lambda x:x["score"],reverse=True)
    return {"asset_id":e["asset_id"],"event_type":e["event_type"],"observed_trip_code":e["trip_code"],
            "hypotheses":hypotheses,"system_consequence":{
              "pumps_available":e["pumps_available_after"],"baseline_sustained":e["baseline_sustained_after"],
              "flow_deficit_m3h":e["flow_deficit_after_m3h"]}}
