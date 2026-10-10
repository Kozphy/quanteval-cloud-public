"""Runtime environment capture for manifests."""

from __future__ import annotations

import importlib.metadata as md
import os
import platform
import resource
import subprocess
from pathlib import Path

PACKAGES = ["quanteval", "numpy", "pandas", "scipy", "statsmodels", "torch", "einops", "huggingface_hub",
            "safetensors", "matplotlib", "jinja2", "weasyprint", "pyarrow", "pyyaml"]

# Google Cloud Run Jobs, Tier-1 default price (https://cloud.google.com/run/pricing, fetched 2026-10-10)
CLOUD_RUN_JOBS_USD_PER_VCPU_S = 0.000018
CLOUD_RUN_JOBS_USD_PER_GIB_S = 0.000002
CLOUD_RUN_JOBS_MIN_BILLED_S = 60.0


def package_versions() -> dict:
    out = {}
    for p in PACKAGES:
        try:
            out[p] = md.version(p)
        except md.PackageNotFoundError:
            out[p] = None
    return out


def cpu_model() -> str:
    try:
        for line in Path("/proc/cpuinfo").read_text().splitlines():
            if line.startswith("model name"):
                return line.split(":", 1)[1].strip()
    except OSError:
        pass
    return platform.processor() or "unknown"


def hardware(threads: int | None) -> dict:
    mem_gib = None
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemTotal"):
                mem_gib = round(int(line.split()[1]) / 1024 / 1024, 2)
    except OSError:
        pass
    return {"platform": platform.platform(), "python": platform.python_version(), "cpu_model": cpu_model(),
            "logical_cpus": os.cpu_count(), "torch_threads": threads, "mem_total_gib": mem_gib}


def peak_rss_gib() -> float:
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024 / 1024  # Linux: KiB


def git_info() -> dict:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists():
            try:
                sha = subprocess.check_output(["git", "-C", str(parent), "rev-parse", "HEAD"], text=True).strip()
                dirty = subprocess.check_output(
                    ["git", "-C", str(parent), "status", "--porcelain", "--", "src", "pyproject.toml"], text=True).strip()
                return {"commit": sha, "dirty_src": bool(dirty)}
            except (subprocess.CalledProcessError, FileNotFoundError):
                break
    return {"commit": None, "dirty_src": None}


def cost_estimate(wall_s: float, vcpus: int, peak_gib: float) -> dict:
    import math

    mem_gib = max(1, math.ceil(peak_gib))
    billed = max(wall_s, CLOUD_RUN_JOBS_MIN_BILLED_S)
    usd = billed * (vcpus * CLOUD_RUN_JOBS_USD_PER_VCPU_S + mem_gib * CLOUD_RUN_JOBS_USD_PER_GIB_S)
    return {
        "basis": "Google Cloud Run Jobs Tier-1 list price, before free tier; https://cloud.google.com/run/pricing (2026-10-10)",
        "assumed_vcpus": vcpus, "assumed_mem_gib": mem_gib, "billed_seconds": round(billed, 1),
        "usd_per_vcpu_s": CLOUD_RUN_JOBS_USD_PER_VCPU_S, "usd_per_gib_s": CLOUD_RUN_JOBS_USD_PER_GIB_S,
        "estimated_usd": round(usd, 5),
        "caveat": "Measured on the QuantEval build box CPU; Cloud Run vCPU speed may differ. "
                  "Excludes container cold start / model download and the monthly free tier.",
    }
