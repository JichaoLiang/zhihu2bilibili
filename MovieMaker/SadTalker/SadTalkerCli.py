import os.path

from safetensors import torch

from MovieMaker.SadTalker.SadTalkerMain import inference

class SadTalkerInputEntity:
    driven_audio = './SadTalkerMain/examples/driven_audio/bus_chinese.wav'
    source_image = './SadTalkerMain/examples/source_image/full_body_1.png'
    ref_eyeblink = None
    ref_pose = None
    checkpoint_dir = './SadTalkerMain/checkpoints'
    result_dir = './SadTalkerMain/results'
    pose_style = 0
    batch_size = 2
    size = 256
    expression_scale = 1.0
    input_yaw = None
    input_pitch = None
    input_roll = None
    enhancer = None
    background_enhancer = None
    cpu = False
    face3dvis = False
    still = False
    preprocess = 'crop'
    verbose = False
    old_version = False
    net_recon = 'resnet50'
    init_path = None
    use_last_fc = False
    bfm_folder = './SadTalkerMain/checkpoints/BFM_Fitting/'
    bfm_model = 'BFM_model_front.mat'
    focal = 1015.0
    center = 112.0
    camera_d = 10.0
    z_near = 5.0
    z_far = 15.0
    device = "cuda"


class SadTalkerCli:
    @staticmethod
    def produceSadTalkerVideoById(characterId, voicePath, toPath: str):

        pass

    @staticmethod
    def produceSadTalkerVideo(characterImagePath, voicePath, toPath: str):
        request = SadTalkerInputEntity()
        request.preprocess = 'full'

        request.driven_audio = voicePath
        request.source_image = characterImagePath #'./SadTalkerMain/examples/source_image/happy.png'
        request.ref_eyeblink = './SadTalkerMain/examples/ref_video/WDA_KatieHill_000.mp4'
        request.ref_pose = './SadTalkerMain/examples/ref_video/shuai.mp4'
        request.still = False
        # request.ref_pose = './SadTalkerMain/examples/ref_video/WDA_KatieHill_000.mp4'
        # request.ref_pose = './SadTalkerMain/examples/ref_video/WDA_AlexandriaOcasioCortez_000.mp4'

        inference.main(request, toPath)
        return toPath
        pass

    @staticmethod
    def produceSadTalkerVideoByEntity(inputentity: SadTalkerInputEntity, toPath: str):
        pass

    @staticmethod
    def test():
        request = SadTalkerInputEntity()
        request.preprocess = 'full'

        request.driven_audio = os.path.abspath('../../Resource/Product/dev/tts_0.wav')
        request.source_image = './SadTalkerMain/examples/source_image/happy.png'
        request.ref_eyeblink = './SadTalkerMain/examples/ref_video/WDA_KatieHill_000.mp4'
        request.ref_pose = './SadTalkerMain/examples/ref_video/shuai.mp4'
        request.still = True
        # request.ref_pose = './SadTalkerMain/examples/ref_video/WDA_KatieHill_000.mp4'
        # request.ref_pose = './SadTalkerMain/examples/ref_video/WDA_AlexandriaOcasioCortez_000.mp4'

        inference.main(request)
        pass
    pass

if __name__ == '__main__':
    img = 'g:/test.png'
    audio = 'r:/output_8.wav'
    to = img + '.mp4'
    SadTalkerCli.produceSadTalkerVideo(img, audio, to)