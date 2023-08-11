import {  loadModel, createEmbedding } from '../src/towelgpt.js'

const embedder = await loadModel("ggml-all-MiniLM-L6-v2-f16.bin", { verbose: true })

console.log(
    createEmbedding(embedder, "Accept your current situation")
)

