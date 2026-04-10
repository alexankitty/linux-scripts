gpu_id="0000:01:00.0"
gpu_audio_id="0000:01:00.1"

basepath="/sys/bus/pci/drivers"

echo -n "$gpu_id" >/sys/bus/pci/drivers/vfio-pci/unbind
echo -n "$gpu_audio_id" >/sys/bus/pci/drivers/vfio-pci/unbind
echo -n "$gpu_audio_id" >/sys/bus/pci/drivers/snd_hda_intel/bind
sleep 3
modprobe amdgpu
