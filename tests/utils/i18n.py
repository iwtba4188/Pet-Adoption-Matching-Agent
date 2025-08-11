class I18n:
    """
    A class to handle internationalization (i18n) for application.

    It loads translation files from a specified folder and provides methods to
    get translated messages.

    Parameters:
        lang (str): The initial language code to set. Defaults to None.
        default_lang (str): The default language code to fall back on. Defaults to "en".
        use_streamlit_lang (bool): Whether to use the Streamlit locale for the initial language. Defaults to True.
        i18n_folder_path (str): The path to the folder containing translation files. Defaults to "./_locales".
    """

    def __init__(
        self,
        lang: str,
        default_lang: str = "en",
        i18n_folder_path: str = "./_locales",
    ) -> None:
        self._i18n_folder_path = i18n_folder_path
        self._translations = self._build_translations()
        self._validate_translations()

        self._lang = ""
        self._default_lang = ""
        self.set_lang(lang)
        self.set_default_lang(default_lang)

    def __call__(self, key: str) -> str:
        """Retrieve the translated message for the given key.

        Arguments:
            key (str): The key for the translation

        Returns:
            str: The translated message
        """
        return self.get_message(key)

    def _validate_translations(self) -> None:
        """
        Validate that translation files exist and meet required format.

        Raises:
            FileNotFoundError: If no translation files are found

        Returns:
            None
        """
        if not self._translations:
            raise FileNotFoundError(
                f"Could not find any translation files in {self._i18n_folder_path}"
            )

    def _build_translations(self) -> dict:
        """
        Build a dictionary of translations from JSON files in the i18n folder.

        Scans the i18n folder path for `messages.json` files and loads them into a dictionary
        where keys are language codes.

        Returns:
            dict: Dictionary of translations with language codes as keys
        """
        import json
        import os

        translations = {}
        for root, _dirs, files in os.walk(self._i18n_folder_path):
            print(f"Checking {root}...")
            if "messages.json" in files:
                lang = os.path.basename(root)
                with open(os.path.join(root, "messages.json"), encoding="utf-8") as f:
                    translations[lang] = json.load(f)

        return translations

    def is_valid_lang(self, lang: str) -> bool:
        """
        Check if the given language code is valid.

        Arguments:
            lang (str): Language code to check

        Returns:
            bool: True if the language code is valid, False otherwise
        """
        return self.match_lang(lang) is not None

    @property
    def lang(self) -> str | None:
        """
        Get the current language code.

        Returns:
            str: The current language code
        """
        return self._lang

    @property
    def default_lang(self) -> str:
        """
        Get the default language code.

        Returns:
            str: The default language code
        """
        return self._default_lang

    def get_valid_languages(self) -> list[str]:
        """
        Get a list of all valid language codes available for translation.

        Returns:
            list[str]: List of available language codes
        """
        return list(self._translations.keys())

    def set_lang(self, lang: str) -> None:
        """
        Set the current language for translations.

        If the specified language is not available, falls back to the default language.

        Arguments:
            lang (str): Language code to set as current language

        Returns:
            None
        """
        self._lang = self.match_lang(lang)
        if self._lang is None:
            self.set_to_default_lang()
            print(
                f"Invalid language '{lang}' specified. Falling back to default language '{self._default_lang}'."
            )

    def set_default_lang(self, lang: str) -> None:
        """
        Set the default language for translations.

        Arguments:
            lang (str): Language code to set as default language

        Returns:
            None

        Raises:
            ValueError: If the specified language is not valid
        """
        if not self.is_valid_lang(lang):
            self._default_lang = "en"
        self._default_lang = lang

    def set_to_default_lang(self) -> None:
        """
        Reset the current language to the default language.

        Returns:
            None
        """
        self._lang = self._default_lang

    def match_lang(self, lang: str) -> str | None:
        """
        Match the given language code to a valid language code.

        This method checks if the provided language code starts with any of the valid language codes
        and returns the most specific match found.

        Arguments:
            lang (str): Language code to match

        Returns:
            str: The most specific valid language code that matches the input
        """
        valid_langs = self.get_valid_languages()
        valid_langs = list(filter(lambda x: lang.startswith(x), valid_langs))

        return sorted(valid_langs, reverse=True)[0] if valid_langs else None

    def get_message(self, key: str) -> str:
        """
        Get a translated message for the given key.

        Attempts to find the translation in the current language first, then falls back
        to the default language if not found. Raises an error if the key doesn't exist in either.

        Arguments:
            key (str): The translation key to look up

        Returns:
            str: The translated message text

        Raises:
            KeyError: If the key is not found in any language
        """
        possible_langs = [self._lang, self._default_lang, "en"]

        for lang in possible_langs:
            if res := self._translations.get(lang, {}).get(key, {}).get("message"):
                return res

        raise KeyError(
            f"Missing translation for key: {key} (lang: {self._lang}, default_lang: {self._default_lang}, 'en')"
        )
