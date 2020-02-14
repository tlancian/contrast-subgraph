cvx_setup
load('../tmp/net.mat')
cvx_solver sedumi
cvx_begin sdp
    variable X(117, 117) symmetric
    maximize trace(P*X)
    subject to
        X >= 0;
        diag(X) == ones(117, 1);
cvx_end
save('../tmp/net.txt', 'X', '-ASCII');
exit;
