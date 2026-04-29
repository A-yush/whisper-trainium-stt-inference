#!/bin/bash
# Monitor Neuron service health and utilization

echo "=========================================="
echo "STT Service Health Monitor"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Check NeuronCore availability
echo "1. NeuronCore Status:"
echo "-------------------------------------------"
if neuron-ls &>/dev/null; then
    echo -e "${GREEN}✓${NC} NeuronCores available"
    neuron-ls | grep -E "NEURON|instance|DEVICE|CORES"
else
    echo -e "${RED}✗${NC} NeuronCores not available"
fi
echo ""

# Check NeuronCore utilization
echo "2. NeuronCore Utilization:"
echo "-------------------------------------------"
if command -v neuron-top &>/dev/null; then
    neuron-top -n 1 2>/dev/null || echo "Unable to get utilization"
else
    echo "neuron-top not available"
fi
echo ""

# Check memory usage
echo "3. System Memory:"
echo "-------------------------------------------"
free -h | grep -E "Mem|Swap"
echo ""

# Check running processes
echo "4. Neuron Processes:"
echo "-------------------------------------------"
ps aux | grep -E "python.*whisper|neuron" | grep -v grep || echo "No Neuron processes found"
echo ""

# Check device status
echo "5. Neuron Device:"
echo "-------------------------------------------"
ls -la /dev/neuron* 2>/dev/null || echo "No Neuron devices found"
echo ""

# Monitor mode (optional)
if [ "$1" == "--watch" ]; then
    echo "Monitoring mode (Ctrl+C to exit)..."
    echo "Refreshing every 5 seconds..."
    echo ""
    while true; do
        clear
        bash $0
        sleep 5
    done
fi
