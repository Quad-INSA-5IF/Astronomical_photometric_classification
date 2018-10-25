from typing import List, Dict

from src import Record
from src import Metadata
from src import CSVReader

from matplotlib import pyplot
from math import log

import numpy as np

def rescale(n: float) -> float:
    if n == 0:
        return n
    else:
        if n < 0:
            return -log(1 + -n)
        else:
            return log(1 + n)


def build_flux_boxplot(class_of: Dict[int, int], time_series: List[Record.Record]) -> None:
    fig = pyplot.figure(figsize=(16, 9.6))
    for i in range(6):
        values_by_target_id = [[] for _ in range(14)]
        for record in time_series:
            if record.passband == i:
                values_by_target_id[class_of[record.id]].append(rescale(record.flux))

        pyplot.subplot(2, 3, i + 1)
        pyplot.boxplot(values_by_target_id)
        pyplot.ylabel("Passband {}".format(PASSBANDS[i]))
        pyplot.xlabel('class')
    fig.suptitle("Flux")
    pyplot.savefig('documentation/flux_boxplot.png')


def build_flux_err_boxplot(class_of: Dict[int, int], time_series: List[Record.Record]) -> None:
    fig = pyplot.figure(figsize=(16, 9.6))
    for i in range(6):
        values_by_target_id = [[] for _ in range(14)]
        for record in time_series:
            if record.passband == i:
                values_by_target_id[class_of[record.id]].append(rescale(abs(record.flux)))

        pyplot.subplot(2, 3, i + 1)
        pyplot.boxplot(values_by_target_id)
        pyplot.ylabel("Passband {}".format(PASSBANDS[i]))
        pyplot.xlabel('class')
    fig.suptitle("Flux Error")
    pyplot.savefig('documentation/flux_err_boxplot.png')


def build_flux_err_ratio_boxplot(class_of: Dict[int, int], time_series: List[Record.Record]) -> None:
    fig = pyplot.figure(figsize=(16, 9.6))
    for i in range(6):
        values_by_target_id = [[] for _ in range(14)]
        for record in time_series:
            if record.passband == i:
                values_by_target_id[class_of[record.id]].append(rescale(abs(record.flux_err / record.flux)))

        pyplot.subplot(2, 3, i + 1)
        pyplot.boxplot(values_by_target_id)
        pyplot.ylabel("Passband {}".format(PASSBANDS[i]))
        pyplot.xlabel('class')
    fig.suptitle("Flux err / flux value")
    pyplot.savefig('documentation/flux_err_ratio_boxplot.png')


def build_flux_err_ratio_over_class_std_boxplot(class_of: Dict[int, int], time_series: List[Record.Record]) -> None:
    fig = pyplot.figure(figsize=(16, 9.6))
    for i in range(6):
        values_by_target_id = [[] for _ in range(14)]
        for record in time_series:
            if record.passband == i:
                values_by_target_id[class_of[record.id]].append(record.flux)

        std_by_target_class = [np.std(values_by_target_id[i]) for i in range(14)]
        ratio_over_std = [[] for _ in range(14)]
        for record in time_series:
            if record.passband == i:
                std_of_target_class = std_by_target_class[class_of[record.id]]
                ratio_over_std[class_of[record.id]].append(rescale(record.flux_err / std_of_target_class))

        pyplot.subplot(2, 3, i + 1)
        pyplot.boxplot(ratio_over_std)
        pyplot.ylabel("Passband {}".format(PASSBANDS[i]))
        pyplot.xlabel('class')
    fig.suptitle("Flux err / class std")
    pyplot.savefig('documentation/flux_err_ratio_over_std_boxplot.png')


if __name__ == '__main__':
    PASSBANDS = ['U', 'G', 'R', 'I', 'Z', 'Y']
    metadata = CSVReader.read_csv("dataset/training_set_metadata.csv", True, lambda line: Metadata.from_line(line))
    time_series = CSVReader.read_csv("dataset/training_set.csv", True, lambda line: Record.from_line(line))

    class_of = {}
    for data in metadata:
        class_of[data.uuid] = data.target

    build_flux_boxplot(class_of, time_series)
    build_flux_err_boxplot(class_of, time_series)
    build_flux_err_ratio_boxplot(class_of, time_series)
    build_flux_err_ratio_over_class_std_boxplot(class_of, time_series)
