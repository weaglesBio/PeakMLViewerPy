# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['PeakMLViewerPy.py'],
             pathex=['/Users/marianne/Documents/Will_MSC/Source/MetabolomicModellingMSc'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='PeakMLViewerPy',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None , icon='favicon.png')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='PeakMLViewerPy')
app = BUNDLE(coll,
             name='PeakMLViewerPy.app',
             icon='favicon.png',
             bundle_identifier=None)
