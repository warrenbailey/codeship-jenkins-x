import argparse
import yaml

codeship_pro_steps = "codeship-steps.yml"
codeship_pro_services = "codeship-services.yml"
jenkins_x_yaml = "jenkins_x.yaml"


def read_codeship_pro_yaml(directory):
    # TODO file exists error handling
    with open(f"{directory}/{codeship_pro_steps}", 'r') as stream:
        try:
            steps = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    with open(f"{directory}/{codeship_pro_services}", 'r') as stream:
        try:
            services = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
    return steps, services


def convert_to_jenkins_x_yaml(jx_steps):
    jenkins_x = {
                 "buildPack": "none",
                 "pipelineConfig": {
                     "pipelines": {
                         "pullRequest": {
                             "pipeline": {
                                 "stages": [{
                                     "name": "codeship-build",
                                     "agent": {
                                         "image": jx_steps[0].get("image"),
                                     },
                                     "steps": jx_steps
                                }]
                            },
                        }
                     }
                 }
                }
    return jenkins_x


def write_to_jenkins_x_file(directory, jenkins_x):
    with open(f"{directory}/jenkins-x.yml", 'w') as stream:
        try:
            yaml.dump(jenkins_x, stream)
        except yaml.YAMLError as exc:
            print(exc)


def convert_to_jx_step(step, services):
    name = step.get("name")
    service = step.get("service")
    command_and_args = step.get("command")
    temp = command_and_args.split()
    command = temp[0]
    command_args = temp[1:]

    image = services.get(service).get("image")

    jx_step = {"name": name, "image": image, "command": command, "args": command_args}
    return jx_step


def run():
    steps, services = read_codeship_pro_yaml(args.input_dir)

    jx_steps = [convert_to_jx_step(step, services) for step in steps]

    jx_data = convert_to_jenkins_x_yaml(jx_steps)
    write_to_jenkins_x_file(args.output_dir, jx_data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert codeship pro yaml')

    parser.add_argument('--input-dir', dest='input_dir', default='.',
                        help='The directory containing the codeship pro yaml')

    parser.add_argument('--output-dir', dest='output_dir', default='.',
                        help='The directory to write the jenkins x yaml')
    args = parser.parse_args()

    run()






