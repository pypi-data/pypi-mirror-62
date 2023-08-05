depends = ('ITKPyBase', 'ITKThresholding', )
templates = (
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('VotingBinaryImageFilter', 'itk::VotingBinaryImageFilter', 'itkVotingBinaryImageFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('BinaryMedianImageFilter', 'itk::BinaryMedianImageFilter', 'itkBinaryMedianImageFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('LabelVotingImageFilter', 'itk::LabelVotingImageFilter', 'itkLabelVotingImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('LabelVotingImageFilter', 'itk::LabelVotingImageFilter', 'itkLabelVotingImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('LabelVotingImageFilter', 'itk::LabelVotingImageFilter', 'itkLabelVotingImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('LabelVotingImageFilter', 'itk::LabelVotingImageFilter', 'itkLabelVotingImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('VotingBinaryHoleFillingImageFilter', 'itk::VotingBinaryHoleFillingImageFilter', 'itkVotingBinaryHoleFillingImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('VotingBinaryHoleFillingImageFilter', 'itk::VotingBinaryHoleFillingImageFilter', 'itkVotingBinaryHoleFillingImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('VotingBinaryHoleFillingImageFilter', 'itk::VotingBinaryHoleFillingImageFilter', 'itkVotingBinaryHoleFillingImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('VotingBinaryHoleFillingImageFilter', 'itk::VotingBinaryHoleFillingImageFilter', 'itkVotingBinaryHoleFillingImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('VotingBinaryHoleFillingImageFilter', 'itk::VotingBinaryHoleFillingImageFilter', 'itkVotingBinaryHoleFillingImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('VotingBinaryHoleFillingImageFilter', 'itk::VotingBinaryHoleFillingImageFilter', 'itkVotingBinaryHoleFillingImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('VotingBinaryIterativeHoleFillingImageFilter', 'itk::VotingBinaryIterativeHoleFillingImageFilter', 'itkVotingBinaryIterativeHoleFillingImageFilterIUC2', True, 'itk::Image< unsigned char,2 >'),
  ('VotingBinaryIterativeHoleFillingImageFilter', 'itk::VotingBinaryIterativeHoleFillingImageFilter', 'itkVotingBinaryIterativeHoleFillingImageFilterIUC3', True, 'itk::Image< unsigned char,3 >'),
  ('VotingBinaryIterativeHoleFillingImageFilter', 'itk::VotingBinaryIterativeHoleFillingImageFilter', 'itkVotingBinaryIterativeHoleFillingImageFilterIUS2', True, 'itk::Image< unsigned short,2 >'),
  ('VotingBinaryIterativeHoleFillingImageFilter', 'itk::VotingBinaryIterativeHoleFillingImageFilter', 'itkVotingBinaryIterativeHoleFillingImageFilterIUS3', True, 'itk::Image< unsigned short,3 >'),
  ('VotingBinaryIterativeHoleFillingImageFilter', 'itk::VotingBinaryIterativeHoleFillingImageFilter', 'itkVotingBinaryIterativeHoleFillingImageFilterISS2', True, 'itk::Image< signed short,2 >'),
  ('VotingBinaryIterativeHoleFillingImageFilter', 'itk::VotingBinaryIterativeHoleFillingImageFilter', 'itkVotingBinaryIterativeHoleFillingImageFilterISS3', True, 'itk::Image< signed short,3 >'),
)
snake_case_functions = ('label_voting_image_filter', 'voting_binary_image_filter', 'voting_binary_iterative_hole_filling_image_filter', 'voting_binary_hole_filling_image_filter', 'binary_median_image_filter', )
