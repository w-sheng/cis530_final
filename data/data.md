## Data

In this project, we attempt two tasks: 
* poetry generation
* meter classification

### Poetry Generation

For poetry generation, we need poems for our models to train on in order to generate new poems. As of now, we have two genres of poems written by two drastically different authors: 
1. Shakespeare Sonnets - 154 sonnets all written in iambic pentameter. These are in [shakespeare_sonnets.txt](shakespeare_sonnets.txt), which are sourced from this [website](http://www.opensourceshakespeare.org/views/sonnets/sonnet_view.php?Sonnet=all&pleasewait=1&msg=pl&fbclid=IwAR1FoO-Fi3p7420tCd3CvmpBn_Rp4AvPGX3PxN_c4ArHBqg2Gu-yjapLoXU). A sample sonnet is the following: 
```From fairest creatures we desire increase,
That thereby beauty's rose might never die,
But as the riper should by time decease,
His tender heir might bear his memory:
But thou, contracted to thine own bright eyes,
Feed'st thy light'st flame with self-substantial fuel,
Making a famine where abundance lies,
Thyself thy foe, to thy sweet self too cruel.
Thou that art now the world's fresh ornament
And only herald to the gaudy spring,
Within thine own bud buriest thy content
And, tender churl, makest waste in niggarding.
Pity the world, or else this glutton be,
To eat the world's due, by the grave and thee.
```

2. Shel Silverstein Poems - 46 poems written by Shel Silverstein, who does not follow a specific meter. These are in [silverstein_poems.txt](silverstein_poems.txt) and were taken and parsed from this [website](http://thewhynot100.blogspot.com/2014/05/46-short-and-sweet-shel-silverstein.html). A sample poem is the following: 
```I will not play tug o’ war.
I’d rather play hug o’ war,
Where everyone hugs
Instead of tugs,
Where everyone giggles
And rolls on the rug,
Where everyone kisses,
And everyone grins,
And everyone cuddles,
And everyone wins.
```
We will expand this reservoir to include other poems of different meters to have more data to work with. 

### Meter Classification

We are classifying whether lines are in iambic pentameter so our train, test, and dev data will be lines of poems that are marked with 1s or 0s. All the data are `.txt` files in their respective `/dev`, `/test`, and `/train` folders within this `/data` folder. A line in any of these files looks like: 
```
These poor rude lines of thy deceased lover,	1
```
The line in the poem and its label are tab separated. 