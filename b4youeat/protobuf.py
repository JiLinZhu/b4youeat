import logging
import os
from typing import Final, List
log = logging.getLogger(__name__)

SCHEMA_DIR: Final = "b4youeat/schema"
OUTPUT_SUBDIR: Final = "b4youeat/proto"
TARGET_DIR: Final = "b4youeat"

class GenerateProtobuf:
    def run(self) -> None:
        log.info("Generated protobuf python binding.")

        input_files = []
        for dir, _, files in os.walk(SCHEMA_DIR):
            input_files.extend(
                [
                    os.path.join(dir, proto_file)
                    for proto_file in files
                    if self._is_proto_file(proto_file)
                ]
            )


        self._compile_protoc(input_files=input_files, target_dir=TARGET_DIR)



    @staticmethod
    def _is_proto_file(file: str) -> bool:
        _, ext = os.path.splitext(file)
        return ext == ".proto"
    

    def _compile_protoc(self, input_files: List[str], target_dir: str) -> None:
        protoc_executable = ["python", "-m grpc_tools.protoc"]
        # schema_packages = self._get_schema_packages()

        # output_dirs = [
        #     os.path.join(target_dir, package, OUTPUT_SUBDIR)
        #     for package in schema_packages
        # ]

        command_lines = [
            *protoc_executable,
            f"--proto_path={SCHEMA_DIR}",
            f"--python_out={target_dir}",
            f"--grpc_python_out={target_dir}"
        ]

        command_lines.extend(input_files)

        command_line = " ".join(command_lines)

        result_code = os.system(command_line)

        if result_code != 0:
            raise Exception("failed to execute protoc")


    def _get_schema_packages(self) -> List[str]:
        ignore_names = frozenset(["__pycache__"])

        return [
            name
            for name in os.listdir(SCHEMA_DIR)
            if os.path.isdir(os.path.join(SCHEMA_DIR, name))
            and name not in ignore_names
        ]
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,)
    c = GenerateProtobuf()
    c.run()