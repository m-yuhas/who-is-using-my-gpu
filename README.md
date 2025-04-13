# Who is using my GPU!?
This application monitors a fleet of GPUs and displays the current status and historical data for each on a dashboard.  You shouldn't use it, there are better tools that weren't thrown together in a weekend like [SLURM](https://slurm.schedmd.com/), which also includes metric reporting.  The goal of this application is to provide a turnkey solution to monitor and deploy tasks to remote systems that are not controlled by any centralized resource management system.

## Quick Start

```
docker compose build
```

```
docker compose up
```

## Architecture
