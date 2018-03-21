
import factory

from Aplications.orgtecol.models import Region


class RegionFactory(factory.DjangoModelFactory):
    class Meta:
        model = Region

    reg_nombre = factory.Faker('sentence', nb_words=4)