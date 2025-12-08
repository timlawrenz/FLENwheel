#!/bin/bash
# Quick browser for training samples organized by checkpoint

EVAL_DIR="$HOME/source/activity/FLENwheel/data/t01p/flux/v1/evaluation"

echo "🔍 FLENwheel Training Sample Browser"
echo "===================================="
echo ""
echo "Organized samples by checkpoint:"
echo ""

for checkpoint in "$EVAL_DIR"/*; do
    if [ -d "$checkpoint" ]; then
        name=$(basename "$checkpoint")
        count=$(ls -1 "$checkpoint"/*.jpg 2>/dev/null | wc -l)
        echo "📁 $name: $count images"
    fi
done

echo ""
echo "💡 To view samples:"
echo "   eog $EVAL_DIR/step_3000_final/*.jpg"
echo "   (or use your preferred image viewer)"
echo ""
echo "📊 Compare checkpoints side-by-side:"
echo "   eog $EVAL_DIR/step_0000_baseline/business_suit.jpg \\"
echo "       $EVAL_DIR/step_1000/business_suit.jpg \\"
echo "       $EVAL_DIR/step_2000/business_suit.jpg \\"
echo "       $EVAL_DIR/step_3000_final/business_suit.jpg"
