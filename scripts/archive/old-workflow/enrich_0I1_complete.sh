#!/bin/bash
# 0I1 Character Enrichment - Master Workflow
# Orchestrates portrait and pose generation

set -e

SCRIPTS_DIR="$HOME/source/activity/FLENwheel/scripts"
DATA_DIR="$HOME/source/activity/FLENwheel/data/0I1"

echo "======================================================================"
echo "0I1 Character Enrichment - Complete Workflow"
echo "======================================================================"
echo ""
echo "📁 Source images: 15"
echo "🎯 Target enriched: 40-50 images"
echo ""
echo "Phase 1: Portrait close-ups (11 images)"
echo "Phase 2: Pose variations (10 images)"
echo "Phase 3: Organize into training dataset"
echo ""
echo "⏱️  Estimated time: 2-3 hours"
echo ""
read -p "Press Enter to start enrichment..."

cd "$HOME/source/activity/FLENwheel"
source venv/bin/activate

echo ""
echo "======================================================================"
echo "PHASE 1: Portrait Close-ups"
echo "======================================================================"
echo ""
python3 "$SCRIPTS_DIR/enrich_0I1_portraits.py"

echo ""
echo "======================================================================"
echo "PHASE 2: Pose Variations"
echo "======================================================================"
echo ""
python3 "$SCRIPTS_DIR/enrich_0I1_poses.py"

echo ""
echo "======================================================================"
echo "PHASE 3: Organize Training Dataset"
echo "======================================================================"
echo ""

# Create training directory
mkdir -p "$DATA_DIR/training"

# Copy source images
echo "📋 Copying source images..."
cp "$DATA_DIR/source"/*.{jpeg,png,jpg} "$DATA_DIR/training/" 2>/dev/null || true

# Copy enriched portraits
echo "📋 Copying enriched portraits..."
cp "$DATA_DIR/enriched/portraits"/*.png "$DATA_DIR/training/" 2>/dev/null || true

# Copy enriched poses
echo "📋 Copying enriched poses..."
cp "$DATA_DIR/enriched/poses"/*.png "$DATA_DIR/training/" 2>/dev/null || true

# Count total
TOTAL=$(ls -1 "$DATA_DIR/training" | wc -l)

echo ""
echo "======================================================================"
echo "✅ ENRICHMENT COMPLETE!"
echo "======================================================================"
echo ""
echo "📊 Training Dataset Summary:"
echo "  - Source images: 15"
echo "  - Enriched portraits: ~11"
echo "  - Enriched poses: ~10"
echo "  - Total training images: $TOTAL"
echo ""
echo "📁 Location: $DATA_DIR/training/"
echo ""
echo "🎯 Next Steps:"
echo "  1. Review enriched images for quality"
echo "  2. Remove any failures/duplicates"
echo "  3. Generate captions (optional)"
echo "  4. Create training config (0I1_v1.yaml)"
echo "  5. Start training!"
echo ""
echo "Recommended training steps: $(($TOTAL * 15))"
echo ""
echo "======================================================================"
