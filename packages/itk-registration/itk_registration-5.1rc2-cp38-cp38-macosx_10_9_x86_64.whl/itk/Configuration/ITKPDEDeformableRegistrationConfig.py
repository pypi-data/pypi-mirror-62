depends = ('ITKPyBase', 'ITKRegistrationCommon', 'ITKFiniteDifference', )
templates = (
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterISS2ISS2IVF22', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterISS3ISS3IVF23', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterISS2ISS2IVF32', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterISS3ISS3IVF33', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterISS2ISS2IVF42', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterISS3ISS3IVF43', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUC2IUC2IVF22', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUC3IUC3IVF23', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUC2IUC2IVF32', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUC3IUC3IVF33', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUC2IUC2IVF42', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUC3IUC3IVF43', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUS2IUS2IVF22', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUS3IUS3IVF23', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUS2IUS2IVF32', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUS3IUS3IVF33', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUS2IUS2IVF42', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIUS3IUS3IVF43', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIF2IF2IVF22', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIF3IF3IVF23', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIF2IF2IVF32', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIF3IF3IVF33', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIF2IF2IVF42', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterIF3IF3IVF43', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterID2ID2IVF22', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterID3ID3IVF23', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterID2ID2IVF32', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterID3ID3IVF33', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterID2ID2IVF42', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('DemonsRegistrationFilter', 'itk::DemonsRegistrationFilter', 'itkDemonsRegistrationFilterID3ID3IVF43', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterISS2ISS2IVF22', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterISS3ISS3IVF23', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterISS2ISS2IVF32', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterISS3ISS3IVF33', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterISS2ISS2IVF42', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterISS3ISS3IVF43', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUC2IUC2IVF22', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUC3IUC3IVF23', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUC2IUC2IVF32', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUC3IUC3IVF33', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUC2IUC2IVF42', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUC3IUC3IVF43', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUS2IUS2IVF22', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUS3IUS3IVF23', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUS2IUS2IVF32', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUS3IUS3IVF33', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUS2IUS2IVF42', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIUS3IUS3IVF43', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIF2IF2IVF22', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIF3IF3IVF23', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIF2IF2IVF32', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIF3IF3IVF33', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIF2IF2IVF42', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterIF3IF3IVF43', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterID2ID2IVF22', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterID3ID3IVF23', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterID2ID2IVF32', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterID3ID3IVF33', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterID2ID2IVF42', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('LevelSetMotionRegistrationFilter', 'itk::LevelSetMotionRegistrationFilter', 'itkLevelSetMotionRegistrationFilterID3ID3IVF43', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('MultiResolutionPDEDeformableRegistration', 'itk::MultiResolutionPDEDeformableRegistration', 'itkMultiResolutionPDEDeformableRegistrationIF2IF2IVF22F', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,2 >, 2 >, float'),
  ('MultiResolutionPDEDeformableRegistration', 'itk::MultiResolutionPDEDeformableRegistration', 'itkMultiResolutionPDEDeformableRegistrationIF3IF3IVF33F', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,3 >, 3 >, float'),
  ('MultiResolutionPDEDeformableRegistration', 'itk::MultiResolutionPDEDeformableRegistration', 'itkMultiResolutionPDEDeformableRegistrationID2ID2IVF22D', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,2 >, 2 >, double'),
  ('MultiResolutionPDEDeformableRegistration', 'itk::MultiResolutionPDEDeformableRegistration', 'itkMultiResolutionPDEDeformableRegistrationID3ID3IVF33D', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,3 >, 3 >, double'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterISS2ISS2IVF22', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterISS3ISS3IVF23', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterISS2ISS2IVF32', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterISS3ISS3IVF33', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterISS2ISS2IVF42', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterISS3ISS3IVF43', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUC2IUC2IVF22', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUC3IUC3IVF23', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUC2IUC2IVF32', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUC3IUC3IVF33', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUC2IUC2IVF42', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUC3IUC3IVF43', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUS2IUS2IVF22', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUS3IUS3IVF23', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUS2IUS2IVF32', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUS3IUS3IVF33', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUS2IUS2IVF42', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIUS3IUS3IVF43', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIF2IF2IVF22', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIF3IF3IVF23', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIF2IF2IVF32', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIF3IF3IVF33', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIF2IF2IVF42', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterIF3IF3IVF43', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterID2ID2IVF22', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterID3ID3IVF23', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterID2ID2IVF32', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterID3ID3IVF33', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterID2ID2IVF42', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('PDEDeformableRegistrationFilter', 'itk::PDEDeformableRegistrationFilter', 'itkPDEDeformableRegistrationFilterID3ID3IVF43', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterISS2ISS2IVF22', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterISS3ISS3IVF23', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterISS2ISS2IVF32', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterISS3ISS3IVF33', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterISS2ISS2IVF42', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterISS3ISS3IVF43', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUC2IUC2IVF22', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUC3IUC3IVF23', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUC2IUC2IVF32', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUC3IUC3IVF33', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUC2IUC2IVF42', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUC3IUC3IVF43', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUS2IUS2IVF22', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUS3IUS3IVF23', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUS2IUS2IVF32', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUS3IUS3IVF33', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUS2IUS2IVF42', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIUS3IUS3IVF43', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIF2IF2IVF22', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIF3IF3IVF23', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIF2IF2IVF32', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIF3IF3IVF33', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIF2IF2IVF42', True, 'itk::Image< float,2 >, itk::Image< float,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterIF3IF3IVF43', True, 'itk::Image< float,3 >, itk::Image< float,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterID2ID2IVF22', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,2 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterID3ID3IVF23', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,2 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterID2ID2IVF32', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,3 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterID3ID3IVF33', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,3 >,3 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterID2ID2IVF42', True, 'itk::Image< double,2 >, itk::Image< double,2 >, itk::Image< itk::Vector< float,4 >,2 >'),
  ('SymmetricForcesDemonsRegistrationFilter', 'itk::SymmetricForcesDemonsRegistrationFilter', 'itkSymmetricForcesDemonsRegistrationFilterID3ID3IVF43', True, 'itk::Image< double,3 >, itk::Image< double,3 >, itk::Image< itk::Vector< float,4 >,3 >'),
)
snake_case_functions = ('pde_deformable_registration_filter', 'symmetric_forces_demons_registration_filter', 'level_set_motion_registration_filter', 'demons_registration_filter', 'multi_resolution_pde_deformable_registration', )
