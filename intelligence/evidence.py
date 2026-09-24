"""Extract observable evidence around Day-2 events without exposing injected causes."""
from statistics import mean

HIDDEN_FIELDS={"failure_cause","scenario"}

def _asset_rows(rows,asset_id,start_s,end_s):
    return [r for r in rows if r["asset_id"]==asset_id and start_s<=r["t_s"]<=end_s]

def event_evidence(rows,asset_id,trip_t_s,lookback_s=30,lookahead_s=5):
    pre=_asset_rows(rows,asset_id,max(0,trip_t_s-lookback_s),trip_t_s-1)
    at=_asset_rows(rows,asset_id,trip_t_s,trip_t_s)
    post=_asset_rows(rows,asset_id,trip_t_s,min(max(r["t_s"] for r in rows),trip_t_s+lookahead_s))
    if not pre or not at:
        raise ValueError("insufficient telemetry around event")
    trip=at[0]
    first,last=pre[0],pre[-1]
    return {
      "asset_id":asset_id,"event_type":"pump_trip","trip_t_s":trip_t_s,
      "trip_code":trip["trip_code"],
      "vibration_start_mm_s":first["vibration_mm_s_rms"],
      "vibration_end_mm_s":last["vibration_mm_s_rms"],
      "vibration_delta_mm_s":round(last["vibration_mm_s_rms"]-first["vibration_mm_s_rms"],3),
      "load_index_start":first["current_load_index"],
      "load_index_end":last["current_load_index"],
      "load_index_delta":round(last["current_load_index"]-first["current_load_index"],4),
      "mean_pretrip_vibration_mm_s":round(mean(r["vibration_mm_s_rms"] for r in pre),3),
      "demand_change_m3h":round(last["demand_m3h"]-first["demand_m3h"],3),
      "pumps_available_after":post[-1]["pumps_available"],
      "delivered_flow_after_m3h":post[-1]["delivered_flow_m3h"],
      "header_head_after_m":post[-1]["header_head_m"],
      "baseline_sustained_after":post[-1]["baseline_sustained"],
      "flow_deficit_after_m3h":post[-1]["flow_deficit_m3h"],
    }

def diagnostic_view(row):
    """Return a telemetry row safe for diagnosis; injected labels stay hidden."""
    return {k:v for k,v in row.items() if k not in HIDDEN_FIELDS}
