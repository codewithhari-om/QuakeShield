
from obspy import Stream
import seisbench.models as sbm


class PhaseNetDetector:
    """Run pretrained PhaseNet to pick seismic phases."""

    def __init__(self, model_name="geofon"):
        self.model = sbm.PhaseNet.from_pretrained(model_name)

    def detect_phases(
        self,
        stream: Stream,
        p_threshold=0.3,
        s_threshold=0.3,
    ):
        """Return structured P- and S-phase picks."""

        if not stream:
            raise ValueError("Input stream is empty.")

        output = self.model.classify(
            stream.copy(),
            P_threshold=p_threshold,
            S_threshold=s_threshold,
            strict=False,
        )

        results = []

        for pick in output.picks:
            results.append({
                "phase": str(pick.phase),
                "time_utc": str(pick.peak_time),
                "confidence": float(pick.peak_value),
                "trace_id": str(pick.trace_id),
            })

        return results
