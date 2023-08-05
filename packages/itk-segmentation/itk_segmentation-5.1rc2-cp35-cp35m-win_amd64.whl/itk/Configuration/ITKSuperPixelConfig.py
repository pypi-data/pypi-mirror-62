depends = ('ITKPyBase', 'ITKStatistics', 'ITKImageSources', 'ITKImageGrid', 'ITKCommon', )
templates = (
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterISS2IULL2', True, 'itk::Image< signed short,2 >, itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterISS3IULL3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterISS2IUS2', True, 'itk::Image< signed short,2 >, itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterISS3IUS3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUC2IULL2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUC3IULL3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUC2IUS2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUC3IUS3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUS2IULL2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUS3IULL3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIF2IULL2', True, 'itk::Image< float,2 >, itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIF3IULL3', True, 'itk::Image< float,3 >, itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIF2IUS2', True, 'itk::Image< float,2 >, itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterIF3IUS3', True, 'itk::Image< float,3 >, itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterID2IULL2', True, 'itk::Image< double,2 >, itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterID3IULL3', True, 'itk::Image< double,3 >, itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterID2IUS2', True, 'itk::Image< double,2 >, itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterID3IUS3', True, 'itk::Image< double,3 >, itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVISS2IULL2', True, 'itk::VectorImage< signed short,2 >,itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVISS2IUS2', True, 'itk::VectorImage< signed short,2 >,itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUC2IULL2', True, 'itk::VectorImage< unsigned char,2 >,itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUC2IUS2', True, 'itk::VectorImage< unsigned char,2 >,itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUS2IULL2', True, 'itk::VectorImage< unsigned short,2 >,itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUS2IUS2', True, 'itk::VectorImage< unsigned short,2 >,itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIF2IULL2', True, 'itk::VectorImage< float,2 >,itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIF2IUS2', True, 'itk::VectorImage< float,2 >,itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVID2IULL2', True, 'itk::VectorImage< double,2 >,itk::Image< unsigned long long,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVID2IUS2', True, 'itk::VectorImage< double,2 >,itk::Image< unsigned short,2 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVISS3IULL3', True, 'itk::VectorImage< signed short,3 >,itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVISS3IUS3', True, 'itk::VectorImage< signed short,3 >,itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUC3IULL3', True, 'itk::VectorImage< unsigned char,3 >,itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUC3IUS3', True, 'itk::VectorImage< unsigned char,3 >,itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUS3IULL3', True, 'itk::VectorImage< unsigned short,3 >,itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIUS3IUS3', True, 'itk::VectorImage< unsigned short,3 >,itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIF3IULL3', True, 'itk::VectorImage< float,3 >,itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVIF3IUS3', True, 'itk::VectorImage< float,3 >,itk::Image< unsigned short,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVID3IULL3', True, 'itk::VectorImage< double,3 >,itk::Image< unsigned long long,3 >'),
  ('SLICImageFilter', 'itk::SLICImageFilter', 'itkSLICImageFilterVID3IUS3', True, 'itk::VectorImage< double,3 >,itk::Image< unsigned short,3 >'),
)
snake_case_functions = ('slic_image_filter', 'image_to_image_filter', )
