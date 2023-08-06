from openomics.database import Annotatable
from openomics.transcriptomics import ExpressionData


class SingleNucleotideVariants(ExpressionData, Annotatable):
    pass

class SomaticMutation(ExpressionData, Annotatable):
    def __init__(self, cohort_name, file_path, columns, genes_col_name, gene_index_by, sample_index_by="sample_barcode",
                 transposed=True,
                 log2_transform=False, npartitions=0):
        super(SomaticMutation, self).__init__(cohort_name, file_path, columns=columns, genes_col_name=genes_col_name,
                                              gene_index_by=gene_index_by, sample_index_by=sample_index_by, transposed=transposed,
                                              log2_transform=log2_transform, npartitions=npartitions)
    @classmethod
    def name(cls):
        return cls.__name__


class DNAMethylation(ExpressionData, Annotatable):
    def __init__(self, cohort_name, file_path, columns, genes_col_name, gene_index_by, sample_index_by="sample_barcode",
                 transposed=True,
                 log2_transform=False, npartitions=0):
        super(DNAMethylation, self).__init__(cohort_name, file_path, columns=columns, genes_col_name=genes_col_name,
                                             gene_index_by=gene_index_by, sample_index_by=sample_index_by, transposed=transposed,
                                             log2_transform=log2_transform, npartitions=npartitions)

    @classmethod
    def name(cls):
        return cls.__name__


class CopyNumberVariation(ExpressionData, Annotatable):
    def __init__(self, cohort_name, file_path, columns, genes_col_name, gene_index_by, sample_index_by="sample_barcode",
                 transposed=True,
                 log2_transform=False, npartitions=0):
        super(CopyNumberVariation, self).__init__(cohort_name, file_path, columns=columns,
                                                  genes_col_name=genes_col_name, gene_index_by=gene_index_by,
                                                  sample_index_by=sample_index_by,
                                                  transposed=transposed, log2_transform=log2_transform,
                                                  npartitions=npartitions)

    @classmethod
    def name(cls):
        return cls.__name__
