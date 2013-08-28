from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from django.contrib.auth.models import Permission
from django.utils.encoding import python_2_unicode_compatible


# This allows South to handle our custom 'CharFieldNullable' field.
if 'south' in settings.INSTALLED_APPS:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ["^sitetree\.models\.CharFieldNullable"])


@python_2_unicode_compatible
class ValidationMethod(models.Model):
    """
    The applied instance of the validation method. Contains the parameters/keyword args from the context reference that will be applied to the validation method.
    """
    name = models.CharField(max_length=255, help_text=_('A simple name that can be used to reference this method.'))
    description = models.CharField(max_length=255, help_text=_('A description of what the method is checking.'))
    method_name = models.CharField(max_length=255, help_text=_('The fully qualified method name.'))
    parameters = models.CharField(max_length=255, null=True, blank=True, help_text=_('A JSON struct of the context parameters that should be passed to the validation method.'))
    keyword_args = models.CharField(max_length=255, null=True, blank=True, help_text=_('A JSON struct of keyword args that should be passed to the validation method.'))

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class TreeItemValidationMethod(models.Model):
    """
    Through model. Used to set sort_order so that we can apply multiple validation methods in a specific order.
    """
    validation_method_instance = models.ForeignKey(to=ValidationMethod, help_text=_('The validation method instance.'))
    tree_item = models.ForeignKey(to='TreeItem', help_text=_('The Tree Item.'))
    sort_order = models.IntegerField(help_text=_('Used to set the order that this method will be applied in. Lower numbers are processed first.'))

    def __str__(self):
        return ": ".join([self.validation_method_instance.name, self.tree_item.title])


class CharFieldNullable(models.CharField):
    """We use custom char field to put nulls in SiteTreeItem 'alias' field.
    That allows 'unique_together' directive in Meta to work properly, so
    we don't have two site tree items with the same alias in the same site tree.

    """
    def get_prep_value(self, value):
        if value is not None:
            if value.strip() == '':
                return None
        return self.to_python(value)


@python_2_unicode_compatible
class Tree(models.Model):
    title = models.CharField(_('Title'), max_length=100, help_text=_('Site tree title for presentational purposes.'), blank=True)
    alias = models.CharField(_('Alias'), max_length=80, help_text=_('Short name to address site tree from templates.<br /><b>Note:</b> change with care.'), unique=True, db_index=True)

    class Meta:
        verbose_name = _('Site Tree')
        verbose_name_plural = _('Site Trees')

    def get_title(self):
        return self.title or self.alias

    def __str__(self):
        return self.alias


@python_2_unicode_compatible
class TreeItem(models.Model):
    PERM_TYPE_ANY = 1
    PERM_TYPE_ALL = 2

    PERM_TYPE_CHOICES = (
        (PERM_TYPE_ANY, _('Any')),
        (PERM_TYPE_ALL, _('All'))
    )

    PERMISSIONS_ONLY = 'PO'
    VALIDATORS_ONLY = 'VO'
    PERMISSIONS_AND_VALIDATORS = 'P&V'
    VALIDATORS_AND_PERMISSIONS = 'V&P'
    PERMISSIONS_OR_VALIDATORS = 'P|V'
    VALIDATORS_OR_PERMISSIONS = 'V|P'

    RULE_ORDER_CHOICES = (
        (PERMISSIONS_ONLY, 'Permissions Only'),
        (VALIDATORS_ONLY, 'Validators Only'),
        (PERMISSIONS_AND_VALIDATORS, 'Permissions and Validators'),
        (VALIDATORS_AND_PERMISSIONS, 'Validators and Permissions'),
        (PERMISSIONS_OR_VALIDATORS, 'Permissions or Validators'),
        (VALIDATORS_OR_PERMISSIONS, 'Validators or Permissions'),
    )

    title = models.CharField(_('Title'), max_length=100, help_text=_('Site tree item title. Can contain template variables E.g.: {{ mytitle }}.'))
    hint = models.CharField(_('Hint'), max_length=200, help_text=_('Some additional information about this item that is used as a hint.'), blank=True, default='')
    url = models.CharField(_('URL'), max_length=200, help_text=_('Exact URL or URL pattern (see "Additional settings") for this item.'), db_index=True)
    urlaspattern = models.BooleanField(_('URL as Pattern'), help_text=_('Whether the given URL should be treated as a pattern.<br /><b>Note:</b> Refer to Django "URL dispatcher" documentation (e.g. "Naming URL patterns" part).'), db_index=True, default=False)
    tree = models.ForeignKey(Tree, verbose_name=_('Site Tree'), help_text=_('Site tree this item belongs to.'), db_index=True)
    hidden = models.BooleanField(_('Hidden'), help_text=_('Whether to show this item in navigation.'), db_index=True, default=False)
    alias = CharFieldNullable(_('Alias'), max_length=80, help_text=_('Short name to address site tree item from a template.<br /><b>Reserved aliases:</b> "trunk", "this-children", "this-siblings" and "this-ancestor-children".'), db_index=True, blank=True, null=True)
    description = models.TextField(_('Description'), help_text=_('Additional comments on this item.'), blank=True, default='')
    inmenu = models.BooleanField(_('Show in menu'), help_text=_('Whether to show this item in a menu.'), db_index=True, default=True)
    inbreadcrumbs = models.BooleanField(_('Show in breadcrumb path'), help_text=_('Whether to show this item in a breadcrumb path.'), db_index=True, default=True)
    insitetree = models.BooleanField(_('Show in site tree'), help_text=_('Whether to show this item in a site tree.'), db_index=True, default=True)
    access_loggedin = models.BooleanField(_('Logged in only'), help_text=_('Check it to grant access to this item to authenticated users only.'), db_index=True, default=False)
    access_restricted = models.BooleanField(_('Restrict access to permissions'), help_text=_('Check it to restrict user access to this item, using Django permissions system.'), db_index=True, default=False)
    access_permissions = models.ManyToManyField(Permission, verbose_name=_('Permissions granting access'), blank=True)
    access_perm_type = models.IntegerField(_('Permissions interpretation'), help_text='<b>Any</b> &mdash; user should have any of chosen permissions. <b>All</b> &mdash; user should have all chosen permissions.', choices=PERM_TYPE_CHOICES, default=PERM_TYPE_ANY)
    # These two are for 'adjacency list' model.
    # This is the current approach of tree representation for sitetree.
    parent = models.ForeignKey('self', verbose_name=_('Parent'), help_text=_('Parent site tree item.'), db_index=True, null=True, blank=True)
    sort_order = models.IntegerField(_('Sort order'), help_text=_('Item position among other site tree items under the same parent.'), db_index=True, default=0)

    validation_methods = models.ManyToManyField(to=ValidationMethod, through=TreeItemValidationMethod)
    rule_order = models.CharField(max_length=3, choices=RULE_ORDER_CHOICES, default=PERMISSIONS_ONLY)

    def save(self, force_insert=False, force_update=False, **kwargs):
        """We override parent save method to set item's sort order to its' primary
        key value.

        """
        super(TreeItem, self).save(force_insert, force_update, **kwargs)
        if self.sort_order == 0:
            self.sort_order = self.id
            self.save()

    class Meta:
        verbose_name = _('Site Tree Item')
        verbose_name_plural = _('Site Tree Items')
        unique_together = ('tree', 'alias')

    def __str__(self):
        return self.title
