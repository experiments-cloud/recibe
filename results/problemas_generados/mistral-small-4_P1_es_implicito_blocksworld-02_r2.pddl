(define (problem blocksworld-problema)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (ontable a)
    (ontable d)
    (on c b)
    (ontable b)
    (clear a)
    (clear c)
    (clear d)
    (handempty)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
