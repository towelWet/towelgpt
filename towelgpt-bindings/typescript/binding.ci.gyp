{
  "targets": [
    {
      "target_name": "towelgpt", # towelgpt-ts will cause compile error
      "include_dirs": [
        "<!@(node -p \"require('node-addon-api').include\")",
        "towelgpt-backend",
      ],
      "sources": [ 
        # PREVIOUS VERSION: had to required the sources, but with newest changes do not need to
        #"../../towelgpt-backend/llama.cpp/examples/common.cpp",
        #"../../towelgpt-backend/llama.cpp/ggml.c",
        #"../../towelgpt-backend/llama.cpp/llama.cpp",
        # "../../towelgpt-backend/utils.cpp", 
        "towelgpt-backend/llmodel_c.cpp",
        "towelgpt-backend/llmodel.cpp",
        "prompt.cc",
        "index.cc",
       ],
      "conditions": [
        ['OS=="mac"', {
            'xcode_settings': {
                'GCC_ENABLE_CPP_EXCEPTIONS': 'YES'
            },
            'defines': [
                'LIB_FILE_EXT=".dylib"',
                'NAPI_CPP_EXCEPTIONS',
            ],
            'cflags_cc': [
                "-fexceptions"
            ]
        }],
        ['OS=="win"', {
            'defines': [
                'LIB_FILE_EXT=".dll"',
                'NAPI_CPP_EXCEPTIONS',
            ],
            "msvs_settings": {
                "VCCLCompilerTool": {
                    "AdditionalOptions": [
                        "/std:c++20",
                        "/EHsc",
                  ], 
                },
            },
        }],
        ['OS=="linux"', {
            'defines': [
                'LIB_FILE_EXT=".so"',
                'NAPI_CPP_EXCEPTIONS',
            ],
            'cflags_cc!': [
                '-fno-rtti',
            ],
            'cflags_cc': [
                '-std=c++2a',
                '-fexceptions'
            ]
        }]
      ]
    }]
}
