Write-Host "`n================================================" -ForegroundColor Magenta
Write-Host "         FINAL RBAC VERIFICATION                " -ForegroundColor Magenta
Write-Host "================================================" -ForegroundColor Magenta

Write-Host "`nServiceAccount: db-viewer" -ForegroundColor Yellow
Write-Host "Role: db-readonly" -ForegroundColor Yellow
Write-Host "Resource: dragonflies (dragonflydb.io)" -ForegroundColor Yellow

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  ALLOWED ACTIONS (should be YES)             " -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`nlist dragonflies:" -ForegroundColor White
kubectl auth can-i list dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`nget dragonflies:" -ForegroundColor White
kubectl auth can-i get dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`nwatch dragonflies:" -ForegroundColor White
kubectl auth can-i watch dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "  DENIED ACTIONS (should be NO)               " -ForegroundColor Red
Write-Host "================================================" -ForegroundColor Cyan

Write-Host "`ndelete dragonflies:" -ForegroundColor White
kubectl auth can-i delete dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`ncreate dragonflies:" -ForegroundColor White
kubectl auth can-i create dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`nupdate dragonflies:" -ForegroundColor White
kubectl auth can-i update dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`npatch dragonflies:" -ForegroundColor White
kubectl auth can-i patch dragonflies --as=system:serviceaccount:default:db-viewer

Write-Host "`n================================================" -ForegroundColor Magenta
Write-Host "VERIFICATION COMPLETED!" -ForegroundColor Cyan
Write-Host "If all yes/no match expectations - RBAC is OK!" -ForegroundColor Green
Write-Host "================================================`n" -ForegroundColor Magenta