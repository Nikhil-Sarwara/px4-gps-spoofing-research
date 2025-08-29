#!/bin/bash

# Examples of how to use the Docker environment

echo "PX4 GPS Spoofing Research - Docker Usage Examples"
echo "=================================================="

echo ""
echo "1. Start PX4 SITL (basic simulation):"
echo "   docker-compose -f docker/docker-compose.yml up"

echo ""
echo "2. Start interactive development environment:"
echo "   docker-compose -f docker/docker-compose.yml run px4-gps-spoofing bash"

echo ""
echo "3. Start with Jupyter notebook server:"
echo "   docker-compose -f docker/docker-compose.dev.yml up"
echo "   Then open: http://localhost:8888"

echo ""
echo "4. Run attack simulation:"
echo "   docker-compose -f docker/docker-compose.yml run px4-gps-spoofing attack"

echo ""
echo "5. Build and rebuild image:"
echo "   docker-compose -f docker/docker-compose.yml build"

echo ""
echo "6. View logs:"
echo "   docker-compose -f docker/docker-compose.yml logs -f"

echo ""
echo "7. Stop all services:"
echo "   docker-compose -f docker/docker-compose.yml down"

echo ""
echo "8. Clean up (remove containers and images):"
echo "   docker-compose -f docker/docker-compose.yml down --rmi all -v"

