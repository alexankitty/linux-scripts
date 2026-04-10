gpu_id="0000:04:00.0"
gpu_audio_id="0000:04:00.1"

basepath="/sys/bus/pci/drivers"

rmmod amdgpu

echo -n "$gpu_audio_id" >/sys/bus/pci/drivers/snd_hda_intel/unbind

echo -n "$gpu_id" >/sys/bus/pci/drivers/vfio-pci/bind
echo -n "$gpu_audio_id" >/sys/bus/pci/drivers/vfio-pci/bind
