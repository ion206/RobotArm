from ikpy.chain import Chain

urdf_path = "src/robotControl/robotArm_fixed.urdf"

# Step 1: Check actual file contents being read
with open(urdf_path, "r") as f:
    contents = f.read()
    print("First 500 characters of URDF:")
    print(contents[:500])

# Step 2: Parse with IKPy
chain = Chain.from_urdf_file(
    urdf_path,
    base_elements=["base_stand"],
    active_links_mask=[False, True, True, True, True, False],
    last_link_vector=[0, 0, -0.05]
)

print("Parsed link names:", [link.name for link in chain.links])