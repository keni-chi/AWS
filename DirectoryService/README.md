# DirectoryService

## �T�v

- SimpleAd, Microsoft AD�Ȃǂ����ۂɍ\�z�Ȃǂ��Ă݂��B

- AD���p����

	- �v��
	Redmine��GitLab��ID,Password�����ʂɂ��AAWS ActiveDirectory�ňꌳ�Ǘ��������B

	- �^��
	��̓I�ȁuCognito User Pool��SAML Provider�v���g�����F�ؔF�V�X�e���̎������@�ɂ��Ă̋^��B(�����Ɂ��ڍׁ��̂P�`�R�ɂ���)

		- �T�v
		AWSDirectoryService���g�����Ƃ��O��̏ꍇ�ACognito���g�����Ƃ��Ă�IdP�ƂȂ�T�[�o�p��EC2�𗧂Ă�K�v������A
		���S�ɃT�[�o���X�ȔF�ؔF�A�[�L�e�N�`���͎����ł��Ȃ��̂ł͂Ȃ����B
		����ŁAAWS DirectoryService�ɂ́uAmazon Cloud Directory�AAmazon Cognito Your User Pools�A
		Microsoft AD�ASimple AD�AAD Connector�v�ƂT��ނ���A�ǂꂩ���g���Ă�������ݒ肷��΃T�[�o���X�Ŏ����ł������H

		- �ڍׁi�����ł��Ȃ���������Ȃ��Ǝv�������R�j
		�P�DIAM�̃v���o�C�_�̍쐬���K�v�ł���A���̎��A���^�f�[�^�h�L�������g�̃t�@�C���I��������K�v������ƔF���B
		�Q�D���̃t�@�C����p�ӂ���ɂ́AADFS����SAML�pMetadata(ADFS�T�[�o�[�̃t�F�f���[�V�������^�f�[�^)���_�E�����[�h����K�v������B
		�R�DSAML�pMetadata��p�ӂ��邽�߂ɂ́AEC2���IdP�ƂȂ�T�[�o���K�v�ł͂Ȃ����B�iIdP�ƂȂ�T�[�o��AWS DirectoryService�ő�p�ł��邩�H�j

