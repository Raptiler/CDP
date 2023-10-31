import os
import yaml

def save_pipeline_to_file(pipeline, jobs, filename):
    with open(filename, "w") as file:
        # Write image, services, and stages first
        if "image" in pipeline:
            file.write(f"image: {pipeline['image']}\n")

        if "services" in pipeline:
            file.write("services:\n")
            for service in pipeline["services"]:
                file.write(f"- {service}\n")

        if "stages" in pipeline:
            file.write("stages:\n")
            for stage in pipeline["stages"]:
                file.write(f"- {stage}\n")

        # Then write the job contents
        yaml.dump(jobs, file, default_flow_style=False)

def create_pipeline_script():
    pipeline = {}
    jobs = {}

    # Suggested values
    suggested_images = ["docker:20.10", "python:3.8", "node:14"]
    suggested_services = ["docker:dind", "postgres:11", "redis:5"]

    # Ask for image
    print("Enter the image for the pipeline.")
    print(f"Suggested images: {', '.join(suggested_images)}")
    image = input("Image: ")
    pipeline["image"] = image

    # Ask for services
    add_services = input("Do you want to add services? (yes/no): ").strip().lower()
    if add_services == "yes":
        print("Enter the services for the pipeline. Separate multiple services with a comma.")
        print(f"Suggested services: {', '.join(suggested_services)}")
        services = input("Services: ").split(",")
        pipeline["services"] = [service.strip() for service in services]

    # Ask for stages
    print("Enter the stages for the pipeline. Separate multiple stages with a comma.")
    stages = input("Stages: ").split(",")
    pipeline["stages"] = [stage.strip() for stage in stages]

    # Check if user wants to add a stage
    while True:
        add_stage = input("Do you want to add a stage? (yes/no): ").strip().lower()
        if add_stage == "no":
            break

        # List available templates
        templates_dir = "./templates"
        available_templates = os.listdir(templates_dir)
        print("Available templates:")
        for idx, template in enumerate(available_templates, 1):
            print(f"{idx}. {template}")

        # Ask user for template choice and job name
        template_choice = int(input(f"Select a template (1-{len(available_templates)}): "))
        job_name = input("Enter the job name: ")

        # Load the chosen template
        template_path = os.path.join(templates_dir, available_templates[template_choice - 1])
        print(f"Trying to load template from: {template_path}")

        with open(template_path, "r") as file:
            job_content = yaml.safe_load(file)
            print(job_content)

        # Add the job to the jobs dictionary
        jobs[job_name] = job_content

    return pipeline, jobs

pipeline, jobs = create_pipeline_script()

# Save the pipeline to gitlab-ci.generated
save_pipeline_to_file(pipeline, jobs, "gitlab-ci.generated")

print("Pipeline saved to 'gitlab-ci.generated'")
