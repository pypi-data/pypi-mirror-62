import warnings
from datetime import date
from os import PathLike, path, makedirs, mkdir
from pathlib import Path
from typing import Union, Optional

import pandas as pd

from econuy import frequent, transform
from econuy.retrieval import (cpi, nxr, fiscal_accounts, national_accounts,
                              labor, rxr, commodity_index, reserves)


class Session(object):
    """
    Main class to access download and processing methods.

    Attributes
    ----------
    loc_dir : str or os.PathLike, default 'econuy-data'
        Directory indicating where data will be saved to and retrieved from.
    revise_rows : {'nodup', 'auto', int}
        Defines how to process data updates. An integer indicates how many rows
        to remove from the tail of the dataframe and replace with new data.
        String can either be ``auto``, which automatically determines number of
        rows to replace from the inferred data frequency, or ``nodup``,
        which replaces existing periods with new data.
    force_update : bool, default False
        Whether to force download even if data was recently modified.
    dataset : pd.DataFrame
        Current working dataset. Initialized with an empty dataframe.

    """
    def __init__(self,
                 loc_dir: Union[str, PathLike] = "econuy-data",
                 revise_rows: Union[int, str] = "nodup",
                 force_update: bool = False,
                 dataset: Union[dict, pd.DataFrame] = pd.DataFrame()):
        self.loc_dir = loc_dir
        self.revise_rows = revise_rows
        self.force_update = force_update
        self.dataset = dataset

        if not path.exists(self.loc_dir):
            makedirs(self.loc_dir)

    def get(self,
            dataset: str,
            update: bool = True,
            save: bool = True,
            override: Optional[str] = None,
            **kwargs):
        """
        Main download method.

        Parameters
        ----------
        dataset : {'cpi', 'nxr', 'fiscal', 'naccounts', 'labor', \
                'comm_index', 'rxr_custom', 'rxr_official', 'reserves', \
                'fx_ops'}
            Type of data to download.
        update : bool, default True
            Whether to update an existing dataset.
        save : bool, default True
            Whether to save the dataset.
        override : str, default None
            If not None, overrides the saved dataset's default filename.
        **kwargs
            These arguments are passed to
            :func:`econuy.retrieval.commodity_index.get`. There's only two
            options: ``force_update_weights: bool`` and
            ``force_update_prices: bool`` which are self-explanatory. Generally
            you will need to update prices but not weights since the latter are
            annual and take a long time to download.

        Returns
        -------
        :class:`~econuy.session.Session`
            Loads the pd.DataFrame output into the :attr:`dataset`
            attribute.

        """
        if update is True:
            update_path = Path(self.loc_dir)
        else:
            update_path = None
        if save is True:
            save_path = Path(self.loc_dir)
        else:
            save_path = None

        if dataset == "cpi" or dataset == "prices":
            output = cpi.get(update=update_path,
                             revise_rows=self.revise_rows,
                             save=save_path,
                             force_update=self.force_update,
                             name=override)
        elif dataset == "fiscal":
            output = fiscal_accounts.get(update=update_path,
                                         revise_rows=self.revise_rows,
                                         save=save_path,
                                         force_update=self.force_update,
                                         name=override)
        elif dataset == "nxr":
            output = nxr.get(update=update_path,
                             revise_rows=self.revise_rows,
                             save=save_path,
                             force_update=self.force_update,
                             name=override)
        elif dataset == "naccounts" or dataset == "na":
            output = national_accounts.get(update=update_path,
                                           revise_rows=self.revise_rows,
                                           save=save_path,
                                           force_update=self.force_update,
                                           name=override)
        elif dataset == "labor" or dataset == "labour":
            output = labor.get(update=update_path,
                               revise_rows=self.revise_rows,
                               save=save_path,
                               force_update=self.force_update,
                               name=override)
        elif dataset == "rxr_custom" or dataset == "rxr-custom":
            output = rxr.get_custom(update=update_path,
                                    revise_rows=self.revise_rows,
                                    save=save_path,
                                    force_update=self.force_update,
                                    name=override)
        elif dataset == "rxr_official" or dataset == "rxr-official":
            output = rxr.get_official(update=update_path,
                                      revise_rows=self.revise_rows,
                                      save=save_path,
                                      force_update=self.force_update,
                                      name=override)
        elif dataset == "commodity_index" or dataset == "comm_index":
            output = commodity_index.get(update=update_path,
                                         save=save_path,
                                         name=override,
                                         **kwargs)
        elif dataset == "reserves":
            output = reserves.get_chg(update=update_path,
                                      save=save_path,
                                      name=override)
        elif dataset == "fx_ops" or dataset == "fxops":
            output = reserves.get_operations(update=update_path,
                                             save=save_path,
                                             name=override)
        else:
            warnings.warn("Invalid keyword for 'dataset' parameter.",
                          UserWarning)
            return self

        self.dataset = output

        return self

    def get_tfm(self,
                dataset: str,
                update: bool = True,
                save: bool = True,
                override: Optional[str] = None,
                **kwargs):
        """
        Get frequently used datasets.

        Parameters
        ----------
        dataset : {'inflation', 'fiscal', 'nxr', 'naccounts', 'labor'}
            Type of data to download.
        update : bool, default  True
            Whether to update an existing dataset.
        save : bool, default  True
            Whether to save the dataset.
        override : str, default None
            If not None, overrides the saved dataset's default filename.
        **kwargs
            Keyword arguments passed to functions in
            :mod:`econuy.frequent`.

        Returns
        -------
        :class:`~econuy.session.Session`
            Loads the downloaded dataframe into the :attr:`dataset` attribute.

        """
        if update is True:
            update_path = Path(self.loc_dir)
        else:
            update_path = None
        if save is True:
            save_path = Path(self.loc_dir)
        else:
            save_path = None

        if dataset == "inflation":
            output = frequent.inflation(update=update_path,
                                        save=save_path,
                                        name=override)
        elif dataset == "fiscal":
            output = frequent.fiscal(update=update_path,
                                     save=save_path,
                                     name=override,
                                     **kwargs)
        elif dataset == "nxr":
            output = frequent.exchange_rate(update=update_path,
                                            save=save_path,
                                            name=override,
                                            **kwargs)
        elif dataset == "naccounts" or dataset == "na":
            output = frequent.nat_accounts(update=update_path,
                                           save=save_path,
                                           name=override,
                                           **kwargs)
        elif dataset == "labor" or dataset == "labour":
            output = frequent.labor_mkt(update=update_path,
                                        save=save_path,
                                        name=override,
                                        **kwargs)
        else:
            warnings.warn("Invalid keyword for 'dataset' parameter.",
                          UserWarning)
            return self
        
        self.dataset = output

        return self

    def resample(self, target: str, operation: str = "sum",
                 interpolation: str = "linear"):
        """
        Resample to target frequencies.

        See Also
        --------
        :func:`~econuy.transform.resample`

        """
        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                output = transform.resample(value, target=target,
                                            operation=operation,
                                            interpolation=interpolation)
                self.dataset.update({key: output})
        else:
            output = transform.resample(self.dataset, target=target,
                                        operation=operation,
                                        interpolation=interpolation)
            self.dataset = output

        return self

    def chg_diff(self, operation: str = "chg", period_op: str = "last"):
        """
        Calculate pct change or difference.

        See Also
        --------
        :func:`~econuy.transform.chg_diff`

        """
        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                output = transform.chg_diff(value, operation=operation,
                                            period_op=period_op)
                self.dataset.update({key: output})
        else:
            output = transform.chg_diff(self.dataset, operation=operation,
                                        period_op=period_op)
            self.dataset = output

        return self

    def decompose(self, flavor: str = "both",
                  trading: bool = True, outlier: bool = True,
                  x13_binary: Union[str, PathLike] = "search",
                  search_parents: int = 1):
        """
        Use `X-13 ARIMA <https://www.census.gov/srd/www/x13as/>`_ to
        decompose time series.

        Parameters
        ----------
        flavor : {'both', 'trend', 'seas'}
            Whether to get the trend component, the seasonally adjusted series
            or both.
        trading : bool, default True
            Whether to automatically detect trading days.
        outlier : bool, default True
            Whether to automatically detect outliers.
        x13_binary: str or os.PathLike, default 'search'
            Location of the X13 binary. If ``search`` is used, will attempt to
            find the binary in the project structure.
        search_parents: int, default 1
            If ``search`` is chosen for ``x13_binary``, this parameter controls
            how many parent directories to go up before recursively searching
            for the binary.

        See Also
        --------
        :func:`~econuy.transform.decompose`

        """
        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                result = transform.decompose(value,
                                             trading=trading,
                                             outlier=outlier,
                                             x13_binary=x13_binary,
                                             search_parents=search_parents)
                if flavor == "trend":
                    output = result[0]
                elif flavor == "seas" or type == "seasonal":
                    output = result[1]
                elif flavor == "both":
                    output = result
                else:
                    warnings.warn("'flavor' can be one of 'both', 'trend', or"
                                  "'seas'.", UserWarning)
                    return self

                self.dataset.update({key: output})
        else:
            result = transform.decompose(self.dataset,
                                         trading=trading,
                                         outlier=outlier,
                                         x13_binary=x13_binary,
                                         search_parents=search_parents)
            if flavor == "trend":
                output = result[0]
            elif flavor == "seas" or type == "seasonal":
                output = result[1]
            elif flavor == "both":
                output = result
            else:
                warnings.warn("'flavor' can be one of 'both', 'trend', or"
                              "'seas'.", UserWarning)
                return self

            self.dataset = output

        return self

    def convert(self, flavor: str, update: Union[str, PathLike, None] = None,
                save: Union[str, PathLike, None] = None, **kwargs):
        """
        Convert to other units.

        See Also
        --------
        :func:`~econuy.transform.convert_usd`,
        :func:`~econuy.transform.convert_real`,
        :func:`~econuy.transform.convert_gdp`

        """
        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                if flavor == "usd":
                    output = transform.convert_usd(value, update=update,
                                                   save=save)
                elif flavor == "real":
                    output = transform.convert_real(value, update=update,
                                                    save=save, **kwargs)
                elif flavor == "pcgdp":
                    output = transform.convert_gdp(value, update=update,
                                                   save=save, **kwargs)
                else:
                    warnings.warn("Invalid keyword for 'flavor' parameter.",
                                  UserWarning)
                    return self

                self.dataset.update({key: output})
        else:
            if flavor == "usd":
                output = transform.convert_usd(self.dataset, update=update,
                                               save=save)
            elif flavor == "real":
                output = transform.convert_real(self.dataset, update=update,
                                                save=save, **kwargs)
            elif flavor == "pcgdp" or flavor == "gdp":
                output = transform.convert_gdp(self.dataset, update=update,
                                               save=save, **kwargs)
            else:
                warnings.warn("Invalid keyword for 'flavor' parameter.",
                              UserWarning)
                return self

            self.dataset = output

        return self

    def base_index(self, start_date: Union[str, date],
                   end_date: Union[str, date, None] = None, base: float = 100):
        """
        Scale to a period or range of periods.

        See Also
        --------
        :func:`~econuy.transform.base_index`

        """
        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                output = transform.base_index(value, start_date=start_date,
                                              end_date=end_date, base=base)
                self.dataset.update({key: output})
        else:
            output = transform.base_index(self.dataset, start_date=start_date,
                                          end_date=end_date, base=base)
            self.dataset = output

        return self

    def rolling(self, periods: Optional[int] = None,
                operation: str = "sum"):
        """
        Calculate rolling averages or sums.

        See Also
        --------
        :func:`~econuy.transform.rolling`

        """
        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                output = transform.rolling(value, periods=periods,
                                           operation=operation)
                self.dataset.update({key: output})
        else:
            output = transform.rolling(self.dataset, periods=periods,
                                       operation=operation)
            self.dataset = output

        return self

    def save(self, name: str):
        """
        Save :attr:`dataset` attribute to a CSV.

        """
        name = Path(name).with_suffix("").as_posix()

        if isinstance(self.dataset, dict):
            for key, value in self.dataset.items():
                save_path = (Path(self.loc_dir) /
                             f"{name}_{key}").with_suffix(".csv")
                if not path.exists(path.dirname(save_path)):
                    mkdir(path.dirname(save_path))
                value.to_csv(save_path)
        else:
            save_path = (Path(self.loc_dir) / name).with_suffix(".csv")
            if not path.exists(path.dirname(save_path)):
                mkdir(path.dirname(save_path))
            self.dataset.to_csv(save_path)

    def final(self):
        """
        Return :attr:`dataset` attribute.
        
        """
        return self.dataset
