"""Map transparent diagnostic hypotheses to verification checks, not automatic maintenance commands."""
CHECKS={
 "mechanical_load_or_bearing_degradation":["Review vibration spectrum/trend","Check bearing temperature and lubrication condition","Inspect coupling and pump mechanical freedom","Verify motor current against mechanical load"],
 "electrical_supply_or_cable_fault":["Review phase currents and voltages","Check phase/voltage imbalance and protection records","Inspect cable/termination condition","Perform appropriate insulation/earth-fault checks under approved procedures"],
}

def verification_plan(diagnosis):
    if not diagnosis["hypotheses"]:
        return {"asset_id":diagnosis["asset_id"],"status":"insufficient_evidence","checks":[]}
    top=diagnosis["hypotheses"][0]
    return {"asset_id":diagnosis["asset_id"],"status":"verification_required",
            "leading_hypothesis":top["hypothesis"],"checks":CHECKS.get(top["hypothesis"],[]),
            "note":"Decision support only; verify evidence before maintenance action."}
