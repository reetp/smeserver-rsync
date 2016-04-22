%define name smeserver-rsync
%define version 1.3
%define release 1
Summary: SMEserver rpm for rsync
Name: %{name}
Version: %{version}
Release: %{release}
License: GNU GPL version 2
URL: http://www.contribs.org
Distribution: SME Server
Group: SMEServer/addon
Source: %{name}-%{version}.tar.gz
Packager: Stephen Noble <stephen@dungog.net>
BuildRoot: /var/tmp/%{name}-%{version}
BuildArchitectures: noarch
BuildRequires: e-smith-devtools
Requires: e-smith-release >= 8
AutoReqProv: no

%description
SMEserver rpm for setting up rsync jobs with a server panel

%changelog
* Thu Apr 21 2016 John Crisp <jcrisp@safeandsoundit.co.uk>
- First import to smecontribs

* Thu Jun 8 2006 Stephen Noble <support@dungog.net>
- db option to allow overlaps, db dungog setprop rsync overlap allow
- suggestion added to automate with dungog-cron
- panel simplified, instructions moved to help
- [1.2-7]

* Tue Jun 6 2006 Stephen Noble <support@dungog.net>
- terminate new jobs if rsync is already running
- [1.2-6]

* Wed Apr 5 2006 Stephen Noble <support@dungog.net>
- add include and exclude directories for 'rsync to self'
- [1.2-5]

* Mon Mar 27 2006 Stephen Noble <support@dungog.net>
- expand crontab on saves
- remote is now user@server.net not just server.net
- [1.2-4]

* Tue Mar 14 2006 Stephen Noble <support@dungog.net>
- fixed incorrect crontab permissions
- [1.2-3]

* Mon Oct 24 2005 Stephen Noble <support@dungog.net>
- more bandwidth options
- help, Advanced options
- [1.2-2]

* Thu Sep 15 2005 Stephen Noble <support@dungog.net>
- option to run every 2,4,8,12 hours
- [1.2-1]

* Thu Aug 11 2005 Stephen Noble <support@dungog.net>
- sme 7 version
- [1.0-7]

* Thu Aug 29 2002 Stephen Noble <stephen@dungog.net>
- initial release
- [0.1-1]


%prep
%setup

%build
perl createlinks


%install
rm -rf $RPM_BUILD_ROOT
(cd root ; find . -depth -print | cpio -dump $RPM_BUILD_ROOT)
/sbin/e-smith/genfilelist $RPM_BUILD_ROOT > %{name}-%{version}-filelist
echo "%doc " >> %{name}-%{version}-filelist

%clean
cd ..
rm -rf %{name}-%{version}

%pre
%preun
%post
#new installs
if [ $1 = 1 ] ; then
 /bin/touch /home/e-smith/db/dungog
fi

/bin/chmod 644 /etc/crontab
/etc/e-smith/events/actions/initialize-default-databases

echo ''
echo 'Remote server syntax changed for secure transfers from dungog-rsync-1.2-4'
echo 'you now need to enter the user as well as the server'
echo 'this removes the requirement of having the same user on both servers'
echo 'but you may need to update your existing rules'
echo ''


%postun
#uninstalls
if [ $1 = 0 ] ; then
 /sbin/e-smith/expand-template /etc/crontab
 /bin/rm -rf /usr/bin/dungogrsync-?????
fi

#&upgrades


%files -f %{name}-%{version}-filelist
%defattr(-,root,root)
