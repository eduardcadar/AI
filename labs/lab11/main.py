import data
import train


def k_means_text(inputs, outputs, label_names, pb, n_clusters, max_features=50):
    train_in, train_out, test_in, test_out = data.split_data(inputs, outputs)

    print("---" + pb + "---")
    # word granularity
    feature_names_word_gran, train_word_gran, test_word_gran =\
        data.word_granularity(train_in, test_in)
    classifier = train.train_by_my_algorithm(train_word_gran, max_iterations=100, n_clusters=n_clusters)
    computed_test_indexes = classifier.predict(test_word_gran)
    computed_test_outputs = [label_names[value] for value in computed_test_indexes]
    print('word granularity accuracy:', train.accuracy(test_out, computed_test_outputs))

    # bag of words
    feature_names_bag, train_bag_gram, test_bag_gram = data.bag_of_words(train_in, test_in)
    classifier = train.train_by_my_algorithm(train_bag_gram, max_iterations=100, n_clusters=n_clusters)
    computed_test_indexes = classifier.predict(test_bag_gram)
    computed_test_outputs = [label_names[value] for value in computed_test_indexes]
    print('bag of words accuracy:', train.accuracy(test_out, computed_test_outputs))

    # word granularity n_grams
    feature_names_gran_gram, train_gram_gram, test_gran_gram =\
        data.word_granularity(train_in, test_in, n=2, max_features=max_features)
    classifier = train.train_by_my_algorithm(train_gram_gram, max_iterations=100, n_clusters=n_clusters)
    computed_test_indexes = classifier.predict(test_gran_gram)
    computed_test_outputs = [label_names[value] for value in computed_test_indexes]
    print('word granularity 2-gram accuracy:', train.accuracy(test_out, computed_test_outputs))

    # bag of words n_grams
    feature_names_bag_gram, train_bag_gram, test_bag_gram =\
        data.bag_of_words(train_in, test_in, n=2, max_features=max_features)
    classifier = train.train_by_my_algorithm(train_bag_gram, max_iterations=100, n_clusters=n_clusters)
    computed_test_indexes = classifier.predict(test_bag_gram)
    computed_test_outputs = [label_names[value] for value in computed_test_indexes]
    print('bag of words 2-gram accuracy:', train.accuracy(test_out, computed_test_outputs))


def k_means_numbers(inputs, outputs, label_names, pb, n_clusters, max_features=50):
    train_in, train_out, test_in, test_out = data.split_data(inputs, outputs)

    print("---" + pb + "---")
    classifier = train.train_by_my_algorithm(train_in, max_iterations=100, n_clusters=n_clusters)
    computed_test_indexes = classifier.predict(test_in)
    computed_test_outputs = [label_names[value] for value in computed_test_indexes]
    print('accuracy:', train.accuracy(test_out, computed_test_indexes))


def solve():
    inp_iris, out_iris, label_iris = data.load_data_iris()
    k_means_numbers(inp_iris, out_iris, label_iris, 'IRIS', n_clusters=3)
    inp_spam, out_spam, label_spam = data.load_data('spam.csv')
    k_means_text(inp_spam, out_spam, label_spam, 'SPAM', n_clusters=2)
    inp_reviews, out_reviews, label_reviews = data.load_data('reviews_mixed.csv')
    k_means_text(inp_reviews, out_reviews, label_reviews, 'REVIEWS', n_clusters=2, max_features=50)


solve()
