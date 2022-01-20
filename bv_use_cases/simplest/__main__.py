from capsul import CapsulEngine

with CapsulEngine() as ce:
    pipeline = ce.executable('bv_use_cases.simplest.Simplest')
    execution_id = ce.start(pipeline)
    try:
        ce.wait(execution_id)
        final_status = ce.status(execution_id)
        ce.raise_for_status(execution_id)
    finally:
        ce.dismiss(execution_id)
