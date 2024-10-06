from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.conf import settings
import re


class coffeeShop(models.Model):
    """
    coffee shop information. Each coffeeShop contains a name, cover photo, 
    description, location, hours, and favorites information.
    """
    name = models.CharField(max_length = 50)
    coverPhoto = models.ImageField(upload_to='coffee_photos/')
    desc = models.TextField()
    location = models.CharField(max_length = 255)
    hours = models.CharField(max_length=100)
    favorited_by = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='favorite_coffee_shops', blank=True)
   
    def clean_word(self, word):
        # Remove non-alphanumeric characters, convert to lowercase, etc.
        return re.sub(r'\W+', '', word.lower())
    
    def get_word_freqs(self):
        """
        returns a dictionary containing the frequency of unique word in the coffeeShop name and desc. Words are not case
        sensitive and non alphanumeric chars are removed.
        """
        words = self.name.split() + self.desc.split()
        cleaned = [self.clean_word(word) for word in words]
        word_freqs = {word: cleaned.count(word) for word in set(cleaned)}
        return word_freqs
    
    def get_total_words(self):
        """
        returns the number of words (not unique) in the description and name
        """
        return len(self.name.split()) + len(self.desc.split())

    def __str__(self):
        return self.name


class coffeeShopSearchDoc(models.Model):
    """
    Stores relevant information from each coffee shop for search functionality.
    All words are cleaned to be non case sensitive and non-alphanumeric chars are
    removed. wInTitle is a dict of the words, and the frequency of the word.
    """  
    
    coffee_shop = models.OneToOneField('coffeeShop', on_delete=models.CASCADE, related_name='SearchDoc')
    freqs = models.JSONField(default=dict, blank=True)
    wordTotal = models.IntegerField(default=0) 

    def wordFreqs(self):
        """
        creates a dictionary of all the words in the title,
        and the frequency each appears (as % of total words)
        sets freqs and wordTotal for the model.
        """
        wordFreqs = self.coffee_shop.get_word_freqs()
        totalWords = self.coffee_shop.get_total_words()
        for word in wordFreqs.keys():
            wordFreqs[word] = (wordFreqs[word]/totalWords)
        self.freqs = wordFreqs
        self.wordTotal = totalWords
        #print(f"Word frequencies for {self.coffee_shop.name}: {self.freqs}")
        self.updateGlobalInvertedIndex()
    
    def updateGlobalInvertedIndex(self):
        #print(f"Updating inverted index for: {self.coffee_shop.name}")
        for word in self.freqs.keys():
            entry, created = GlobalInvertedIndex.objects.get_or_create(term=word)

            if self.coffee_shop.id not in entry.coffee_shop_ids:
                entry.coffee_shop_ids.append(self.coffee_shop.id)
                entry.save()


    def save(self, *args, **kwargs):
        """
        overrides the model save so that freqs and wordTotal are
        always updated firstw
        """
        #print(f"Saving coffeeShopSearchDoc for: {self.coffee_shop.name}")
        self.wordFreqs()
        super().save(*args, **kwargs)

    def term_frequency(self, term):       
        """
        given a String target word, finds the frequency within the
        document as a percent of total words. If word isn't present
        returns 0.
        """
        cleaned = self.coffee_shop.clean_word(term)
        if cleaned not in self.freqs:
            return 0
        else:
            return self.freqs[cleaned]

    def get_words(self):
        """
        gets the set of all words present in the coffee Shop title
        """
        return set(self.freqs.keys())

    def __repr__(self):
        return f"Document('{self.coffee_shop.name}')"


class GlobalInvertedIndex(models.Model):
    """
    an inverted index containing entries for all coffeeShops.
    """
    
    term = models.CharField(max_length = 255, unique=True)
    coffee_shop_ids = models.JSONField(default = list)
    
    def  __str__(self):
        return f"InvertedIndex for {self.term}"
    
    
    
#Event information. Each event is linked to one coffee shop. 
# Includes name, description, date, time, and admission cost.
class Event(models.Model):
    coffee_shop = models.ForeignKey(coffeeShop, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=255)
    desc = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    admission_cost = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    def __str__(self):
        return f"{self.title} - {self.coffee_shop.name}"
    class Meta:
        ordering = ['date', 'time']



class stat(models.Model):
    """    
    Coffee shop statistics for categories bookworm, adventurer, averagejoe and accessibility. 
    There is one stat per coffee shop which is manually set.
    """
    coffee_shop = models.OneToOneField('coffeeShop', on_delete=models.CASCADE, related_name='CoffeeStats', null=True)
    bkwrm_val = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)],
            default=50,
            help_text="enter a number between 0 and 100.",
        )
    adv_val = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)],
            default=50,
            help_text="enter a number between 0 and 100.",
        )
    avgj_val = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)],
            default=50,
            help_text="enter a number between 0 and 100.",
        ) 
    acc_val = models.IntegerField(
            validators=[MinValueValidator(0), MaxValueValidator(100)],
            default=50,
            help_text="enter a number between 0 and 100.",
        )
    def __str__(self):
        return f"stats of {self.coffee_shop.name}"
