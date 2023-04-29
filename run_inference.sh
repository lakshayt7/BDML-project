for fullfile in ./traces/*
do
    filename=$(basename -- "$fullfile")
    filename="${filename%.*}"
    
    echo "running on ./traces/${filename}.json storing in ./trace_out/${filename}.out"
    python3 ./CRISP_CPT/inference.py j "./traces/${filename}.json" > "./trace_out/${filename}.out"
done