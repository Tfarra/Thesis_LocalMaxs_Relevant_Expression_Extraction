# Thesis_LocalMaxs_Relevant_Expression_Extraction
My thesis on Relevant Expressions and Keywords extraction, from unstructured texts relying solely on statistics.

The main goal was to improve the LocalMaxs extractor, which retrieves Relevant Expressions from documents regardless of the language. It relies heavily on the value of statistical cohesion among words and sets of words. Briefly, it calculates the glue that puts words together, thus forming a strong expression or not. Words that tend to appear together (and only together) and obey the same pattern along the document, usually form these Relevant Expressions. One the other hand, words that have no particular context and appear scattered indiscriminately throughout the corpus, are of no interest to us.

In the end, the precision score increased from 70% to roughly 85%, and the extractor is now able to retrieve single words, which it couldn't previouly.

To achieve this, I implemented a method that can spot stopwords without semantic assistance. Words that present a very high number of distinct neighbours (words on their left and right) are typically connectors, and convey no useful meaning. This method to extract stopwords showed to be 100% precise, only extracting irrelevant terms!

![neighboursline](https://user-images.githubusercontent.com/48351481/159038560-2633c058-5ecc-40c6-b246-b15ae466e20e.png)

This was tested using Portuguese, English and German corpura, and the language indepence was confirmed, meaning that these patterns occurs, regardless of the language.

Code:

1. Formatting the text.
2. Word and expression count
3. Calculate cohesion values for every expression
4. Execute LocalMaxs, and retrieve candidates to Relevant Expressions
5. Calculate stopwords
6. Use Stopwords to trim the candidates to RE, and now we are left with the final result.
7. Make use of the extracted relevant expressions and prepare to extract keywords.
8. Retrieve Relevant Single Words (keywords)
9. Evaluate recall and precision

