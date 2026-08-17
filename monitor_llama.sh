#!/data/data/com.termux/files/usr/bin/bash

export LLAMA_ARG_NUM_THREADS=4

peak=0

monitor() {
    while true; do
        pid=$(pgrep -n -x llama-bench 2>/dev/null)

        if [ -n "$pid" ] && [ -r "/proc/$pid/status" ]; then
            rss=$(awk '/VmRSS:/ {print $2}' "/proc/$pid/status")

            if [ -n "$rss" ] && [ "$rss" -gt "$peak" ]; then
                peak=$rss
                echo "PEAK_RSS_KB=$peak" >&2
            fi
        fi

        if ! pgrep -x llama-bench >/dev/null 2>&1; then
            sleep 0.1
            if ! pgrep -x llama-bench >/dev/null 2>&1; then
                break
            fi
        fi

        sleep 0.2
    done
}

monitor &
MONITOR_PID=$!

timeout 120s llama-bench \
  -m model/qwen2.5-coder-1.5b-instruct-q4_k_m.gguf \
  -p 32 \
  -n 16 \
  -ngl 0 \
  -t 4 \
  -r 1 \
  --no-warmup \
  --progress \
  -o json

STATUS=$?

kill "$MONITOR_PID" 2>/dev/null
wait "$MONITOR_PID" 2>/dev/null

exit "$STATUS"
