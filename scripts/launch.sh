#!/bin/bash

# KMP_AFF=verbose,granularity=fine,compact,1,0
# BACKEND=pytorch,ov,torchscript
# LOG_BK=pt-ov-tf
# BATCH_SIZE=1
# SEQ_LEN=32,128,256,512
# BENCH_DURATION=20
# WARMUP_RUN=5

# N_INSTS=(1)
# MODELS=(bert-base-cased)

. $1

echo "KMP_AFF is $KMP_AFF"
echo "BACKEND is $BACKEND"
echo "LOG_BK is $LOG_BK"
echo "BATCH_SIZE is $BATCH_SIZE"
echo "SEQ_LEN is $SEQ_LEN"
echo "BENCH_DURATION is $BENCH_DURATION"
echo "WARMUP_RUN is $WARMUP_RUN"
echo "N_INSTS is $N_INSTS"
echo "MODELS is $MODELS"
echo "RUN_RESULTS is $RUN_RESULTS"
echo "MODEL_RESULTS is $MODEL_RESULTS"

#rm -rf outputs
rm -rf $2

# Run benchmark
for MODEL in ${MODELS[@]}; do
    rm -rf outputs
    for N_INST in ${N_INSTS[@]}; do
        cmd_to_run="PYTHONPATH=src python3 launcher.py \
        --multi_instance \
        --ninstances=$N_INST \
        --kmp_affinity=$KMP_AFF \
        --enable_iomp \
        --enable_tcmalloc \
        -- src/main.py \
        --multirun \
        backend=$BACKEND \
        batch_size=$BATCH_SIZE \
        sequence_length=$SEQ_LEN \
        benchmark_duration=$BENCH_DURATION \
        warmup_runs=$WARMUP_RUN \
        model=$MODEL \
        models_path=$MODELS_PATH \
        2>&1 | \
        tee logs/$MODEL-$LOG_BK-instances-$N_INST-dur-$BENCH_DURATION-wup-$WARMUP_RUN.log "

        echo "*** Starting benchmark with :"
        echo $cmd_to_run
        eval $cmd_to_run
    done
    python ./scripts/launch_results_parser.py -i $RUN_RESULTS/default/ -o $MODEL_RESULTS
done;

python ./scripts/parser_with_selec_params.py -i $MODEL_RESULTS/. -c $1

# Parse results
#python ./scripts/launch_results_parser.py -i ./outputs/default/ -o $2

# Plot results
#python ./scripts/plot_results.py -i $2 -o $2
