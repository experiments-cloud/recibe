(define (problem blocksworld-problem)
  (:domain BLOCKS)
  (:objects
    a b c d - block
  )
  (:init
    (clear a)
    (clear c)
    (clear d)
    (handempty)
    (ontable a)
    (ontable b)
    (ontable d)
    (on c b)
  )
  (:goal (and
    (on a b)
    (on b c)
    (on c d)
  ))
)
