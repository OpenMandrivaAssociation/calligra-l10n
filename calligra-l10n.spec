# Supported l10n language
%define langlist bs ca cs da de el en_GB es et fi fr gl hu it ja kk nb nl pl pt pt_BR ru sk sv uk zh_CN zh_TW

# Languages that were once supported, but aren't supported by the current release anymore
# (old packages have to be obsoleted so we don't create dependency problems)
%define temporarily_unsupported tr sl nds

# Language descriptions
%define language_bs bs
%define langname_bs Bosnian
%define language_ca ca
%define langname_ca Catalan
%define language_cs cs
%define langname_cs Czech
%define language_da da
%define langname_da Dansk
%define language_de de
%define langname_de German
%define language_el el
%define langname_el Greek
%define language_en_GB en_GB
%define langname_en_GB British English
%define language_es es
%define langname_es Spanish
%define language_et et
%define langname_et Estonian
%define language_fi fi
%define langname_fi Finnish
%define language_fr fr
%define langname_fr French
%define language_gl gl
%define langname_gl Galician
%define language_hu hu
%define langname_hu Hungarian
%define language_it it
%define langname_it Italian
%define language_ja ja
%define langname_ja Japanese
%define language_kk kk
%define langname_kk Kazakh
%define language_nb nb
%define langname_nb Norwegian
%define language_nl nl
%define langname_nl Dutch
%define language_nds nds
%define langname_nds Lower Saxon
%define language_pl pl
%define langname_pl Polish
%define language_pt pt
%define langname_pt Portuguese
%define language_pt_BR pt_BR
%define langname_pt_BR Brazilian portuguese
%define language_pt_PT pt-PT
%define langname_pt_PT Portuguese
%define language_ru ru
%define langname_ru Russian
%define language_sl sl
%define langname_sl Slovenian
%define language_sk sk
%define langname_sk Slovakian
%define language_sv sv
%define langname_sv Swedish
%define language_tr tr
%define langname_tr Turkish
%define language_uk uk
%define langname_uk Ukrainian
%define language_wa wa
%define langname_wa Walloon
%define language_zh_CN zh_CN
%define langname_zh_CN Simplified Chinese
%define language_zh_TW zh_TW
%define langname_zh_TW Traditional Chinese

# --- Danger line ---

# Locales
%{expand:%(for lang in %langlist; do echo "%%define locale_$lang `echo $lang | cut -d _ -f 1` "; done)}

Summary: Language files for Calligra (virtual package)
Name: calligra-l10n
Version: 2.9.11
Release: 1
License: GPLv2+
Group: System/Internationalization
Url: https://www.calligra-suite.org/
# localisation package template
Source0: %{name}-template.in
Source1: %{name}.rpmlintrc
# l10n sources
%{expand:%(\
	i=2; \
	for lang in %langlist; do\
		echo "%%{expand:Source$i: http://download.kde.org/stable/calligra-%%{version}/%%{name}/%%{name}-%%{language_$lang}-%%{version}.tar.xz}";\
		i=$[i+1];\
	done\
	)
}
BuildRequires: gettext >= 0.15
BuildRequires: kdelibs4-devel
BuildArch: noarch
Obsoletes: koffice-l10n
%{expand:%(\
	for i in %temporarily_unsupported; do \
		echo "Obsoletes: %name-$i < %EVRD"; \
	done)
}

%description
Language files for Calligra.

# Expand all localisation packages descriptions.

%{expand:%(\
	for lang in %langlist; do\
		echo "%%{expand:%%(sed "s!__LANG__!$lang!g" %{_sourcedir}/%{name}-template.in 2> /dev/null)}";\
	done\
	)
}

%prep
%setup -T -n %{name}-%{version} -c

for lang in %langlist; do\
  tar xf %{_sourcedir}/%{name}-$lang-%{version}.tar.xz;
done

%build
for lang in %langlist; do\
	pushd %{name}-$lang-%{version};
		%cmake_kde4 -DCMAKE_MINIMUM_REQUIRED_VERSION=2.6;
		%make;
	popd;
done

%install

for lang in %langlist; do
	pushd %{name}-$lang-%{version};
		%makeinstall_std -C build;
	popd;
done
