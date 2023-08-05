depends = ('ITKPyBase', 'ITKThresholding', 'ITKSmoothing', 'ITKMathematicalMorphology', 'ITKImageIntensity', 'ITKImageGradient', )
templates = (
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterIF2IF2', True, 'itk::Image< float,2 >, itk::Image< float,2 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterIF3IF3', True, 'itk::Image< float,3 >, itk::Image< float,3 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterID2ID2', True, 'itk::Image< double,2 >, itk::Image< double,2 >'),
  ('IsolatedWatershedImageFilter', 'itk::IsolatedWatershedImageFilter', 'itkIsolatedWatershedImageFilterID3ID3', True, 'itk::Image< double,3 >, itk::Image< double,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterISS2IUC2', True, 'itk::Image< signed short,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterISS3IUC3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterISS2IUS2', True, 'itk::Image< signed short,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterISS3IUS3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUC2ISS2', True, 'itk::Image< unsigned char,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUC3ISS3', True, 'itk::Image< unsigned char,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUC2IUS2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUC3IUS3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUS2ISS2', True, 'itk::Image< unsigned short,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUS3ISS3', True, 'itk::Image< unsigned short,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUS2IUC2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUS3IUC3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIF2ISS2', True, 'itk::Image< float,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIF3ISS3', True, 'itk::Image< float,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIF2IUC2', True, 'itk::Image< float,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIF3IUC3', True, 'itk::Image< float,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIF2IUS2', True, 'itk::Image< float,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterIF3IUS3', True, 'itk::Image< float,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterID2ISS2', True, 'itk::Image< double,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterID3ISS3', True, 'itk::Image< double,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterID2IUC2', True, 'itk::Image< double,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterID3IUC3', True, 'itk::Image< double,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterID2IUS2', True, 'itk::Image< double,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedFromMarkersImageFilter', 'itk::MorphologicalWatershedFromMarkersImageFilter', 'itkMorphologicalWatershedFromMarkersImageFilterID3IUS3', True, 'itk::Image< double,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterISS2ISS2', True, 'itk::Image< signed short,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterISS3ISS3', True, 'itk::Image< signed short,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterISS2IUC2', True, 'itk::Image< signed short,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterISS3IUC3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterISS2IUS2', True, 'itk::Image< signed short,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterISS3IUS3', True, 'itk::Image< signed short,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUC2ISS2', True, 'itk::Image< unsigned char,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUC3ISS3', True, 'itk::Image< unsigned char,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUC2IUC2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUC3IUC3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUC2IUS2', True, 'itk::Image< unsigned char,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUC3IUS3', True, 'itk::Image< unsigned char,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUS2ISS2', True, 'itk::Image< unsigned short,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUS3ISS3', True, 'itk::Image< unsigned short,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUS2IUC2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUS3IUC3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUS2IUS2', True, 'itk::Image< unsigned short,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIUS3IUS3', True, 'itk::Image< unsigned short,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIF2ISS2', True, 'itk::Image< float,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIF3ISS3', True, 'itk::Image< float,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIF2IUC2', True, 'itk::Image< float,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIF3IUC3', True, 'itk::Image< float,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIF2IUS2', True, 'itk::Image< float,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterIF3IUS3', True, 'itk::Image< float,3 >, itk::Image< unsigned short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterID2ISS2', True, 'itk::Image< double,2 >, itk::Image< signed short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterID3ISS3', True, 'itk::Image< double,3 >, itk::Image< signed short,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterID2IUC2', True, 'itk::Image< double,2 >, itk::Image< unsigned char,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterID3IUC3', True, 'itk::Image< double,3 >, itk::Image< unsigned char,3 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterID2IUS2', True, 'itk::Image< double,2 >, itk::Image< unsigned short,2 >'),
  ('MorphologicalWatershedImageFilter', 'itk::MorphologicalWatershedImageFilter', 'itkMorphologicalWatershedImageFilterID3IUS3', True, 'itk::Image< double,3 >, itk::Image< unsigned short,3 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterISS2', True, 'itk::Image< signed short,2 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterISS3', True, 'itk::Image< signed short,3 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterIUC2', True, 'itk::Image< unsigned char,2 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterIUC3', True, 'itk::Image< unsigned char,3 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterIUS2', True, 'itk::Image< unsigned short,2 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterIUS3', True, 'itk::Image< unsigned short,3 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterIF2', True, 'itk::Image< float,2 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterIF3', True, 'itk::Image< float,3 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterID2', True, 'itk::Image< double,2 >'),
  ('TobogganImageFilter', 'itk::TobogganImageFilter', 'itkTobogganImageFilterID3', True, 'itk::Image< double,3 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterISS2', True, 'itk::Image< signed short,2 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterISS3', True, 'itk::Image< signed short,3 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterIUC2', True, 'itk::Image< unsigned char,2 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterIUC3', True, 'itk::Image< unsigned char,3 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterIUS2', True, 'itk::Image< unsigned short,2 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterIUS3', True, 'itk::Image< unsigned short,3 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterIF2', True, 'itk::Image< float,2 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterIF3', True, 'itk::Image< float,3 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterID2', True, 'itk::Image< double,2 >'),
  ('WatershedImageFilter', 'itk::WatershedImageFilter', 'itkWatershedImageFilterID3', True, 'itk::Image< double,3 >'),
)
snake_case_functions = ('isolated_watershed_image_filter', 'toboggan_image_filter', 'watershed_image_filter', 'morphological_watershed_image_filter', 'morphological_watershed_from_markers_image_filter', )
