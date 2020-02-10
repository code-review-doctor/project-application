from django.db import models

from project_core.models import CreateModify, Proposal, Call


class CommentType(CreateModify):
    comment_type = models.CharField(max_length=100, help_text='Type of comment', unique=True)

    def __str__(self):
        return self.comment_type


class ProposalCommentType(CreateModify):
    comment_type = models.ForeignKey(CommentType, on_delete=models.PROTECT)

    def __str__(self):
        return self.comment_type.comment_type


class AbstractComment(CreateModify):
    text = models.TextField(help_text='Comment text', null=False,
                            blank=False)

    class Meta:
        unique_together = (('created_on', 'created_by'),)
        abstract = True


class ProposalComment(AbstractComment):
    proposal = models.ForeignKey(Proposal, help_text='Proposal that this comment refers to',
                                 on_delete=models.PROTECT, )
    comment_type = models.ForeignKey(ProposalCommentType, help_text='Type of comment',
                                     on_delete=models.PROTECT)

    class Meta:
        unique_together = (('proposal', 'created_on', 'created_by'),)


class CallComment(AbstractComment):
    """Comments made about a call"""
    call = models.ForeignKey(Call, help_text='Call about which the comment was made', on_delete=models.PROTECT)

    class Meta:
        unique_together = (('call', 'created_on', 'created_by'),)
