import os

content_template = """name: {name}

shape_meta: &shape_meta
  # acceptable types: rgb, low_dim
  obs:
    point_cloud:
      shape: [1024, 6]
      type: point_cloud
    agent_pos:
      shape: [14]
      type: low_dim
  action:
    shape: [14]

env_runner:
  _target_: diffusion_policy_3d.env_runner.robot_runner.RobotRunner
  max_steps: 300
  n_obs_steps: ${{n_obs_steps}}
  n_action_steps: ${{n_action_steps}}
  task_name: robot

dataset:
  _target_: diffusion_policy_3d.dataset.robot_dataset.RobotDataset
  zarr_path: data/{name}.zarr
  horizon: ${{horizon}}
  pad_before: ${{eval:'${{n_obs_steps}}-1'}}
  pad_after: ${{eval:'${{n_action_steps}}-1'}}
  seed: 0
  val_ratio: 0.02
  max_train_episodes: null
"""

names = [
    "tool_adjust_T", 
    "tool_adjust_G", 
    "bottle_adjust_T", 
    "diverse_bottles_pick_G",
    "shoe_place_T",
    "shoe_place_G",
    "shoes_place_T",
    "shoes_place_G"
]

output_dir = "./"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for orig_name in names:
    num = ['100']
    for x in num:
        name = orig_name + '_' + x
        content = content_template.format(name=name)
        file_path = os.path.join(output_dir, f"{name}.yaml")
        with open(file_path, 'w') as file:
            file.write(content)
        print(f"文件已生成: {file_path}")

print("所有文件已生成完毕。")